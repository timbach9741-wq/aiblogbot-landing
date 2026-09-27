// 라이선스 키 서명 서버 (2026-09-27)
//
// 예전 키(PREM-...)는 앱/관리자 페이지에 들어있는 공용 비밀값(SALT)으로 만들어서, 소스를 본
// 사람이면 누구나 자기 PC용 키를 만들 수 있었다. 이제 키는 여기서만 Ed25519 비공개 키로
// 서명하고(비공개 키는 서버 DB 안에만 있음), 앱은 공개 키로 검증만 한다.
//
//   action "activate" : 앱이 활성화 코드(ACT-XXXX-XXXX)를 이 PC에 등록하고 서명된 키를 받는다
//   action "issue"    : 관리자 페이지(관리자 로그인 토큰 필수)가 MAC을 알 때 키를 바로 발급한다
//
// 키 형식: PRO-<만료일 YYMMDD>-<"MAC|YYMMDD"에 대한 서명, base64url 86자>

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ADMIN_EMAIL = "timbach9741@gmail.com";
const MAC_RE = /^[0-9A-F]{2}([-:][0-9A-F]{2}){5}$/;

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// 서명 키는 서버가 처음 실행될 때 스스로 만들어 license_signing_keys 표(서비스 키로만
// 접근 가능)에 보관한다. 비공개 키가 서버 밖으로 나갈 일이 아예 없다.
const REST_HEADERS = { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}`, "Content-Type": "application/json" };
const b64 = (bytes: Uint8Array) => btoa(String.fromCharCode(...bytes));

async function readKeyRow() {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/license_signing_keys?id=eq.1&select=private_pkcs8,public_raw`, { headers: REST_HEADERS });
  const rows = await res.json();
  return Array.isArray(rows) && rows.length ? rows[0] : null;
}

let keysPromise: Promise<{ priv: CryptoKey; pub: string }> | null = null;
function keys() {
  if (!keysPromise) {
    keysPromise = (async () => {
      let row = await readKeyRow();
      if (!row) {
        const kp = (await crypto.subtle.generateKey({ name: "Ed25519" }, true, ["sign", "verify"])) as CryptoKeyPair;
        await fetch(`${SUPABASE_URL}/rest/v1/license_signing_keys`, {
          method: "POST",
          headers: { ...REST_HEADERS, Prefer: "resolution=ignore-duplicates,return=minimal" },
          body: JSON.stringify({
            id: 1,
            private_pkcs8: b64(new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey))),
            public_raw: b64(new Uint8Array(await crypto.subtle.exportKey("raw", kp.publicKey))),
          }),
        });
        row = await readKeyRow(); // 동시에 두 곳에서 만들었어도 먼저 저장된 하나만 쓴다
      }
      if (!row) throw new Error("signing key unavailable");
      const der = Uint8Array.from(atob(row.private_pkcs8), (c) => c.charCodeAt(0));
      const priv = await crypto.subtle.importKey("pkcs8", der, { name: "Ed25519" }, false, ["sign"]);
      return { priv, pub: row.public_raw as string };
    })();
    keysPromise.catch(() => { keysPromise = null; });
  }
  return keysPromise;
}

function base64url(bytes: Uint8Array) {
  return b64(bytes).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function makeKey(mac: string, expiry: string) {
  const data = new TextEncoder().encode(`${mac}|${expiry}`);
  const sig = new Uint8Array(await crypto.subtle.sign("Ed25519", (await keys()).priv, data));
  return `PRO-${expiry}-${base64url(sig)}`;
}

// 관리자 페이지와 같은 기준: 한국 시간 오늘 + days
function expiryFromDays(days: number) {
  const d = new Date(Date.now() + 9 * 3600_000 + days * 86400_000);
  const p = (n: number) => String(n).padStart(2, "0");
  return p(d.getUTCFullYear() % 100) + p(d.getUTCMonth() + 1) + p(d.getUTCDate());
}

async function isAdmin(authHeader: string | null) {
  if (!authHeader) return false;
  const res = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { apikey: SERVICE_KEY, Authorization: authHeader },
  });
  if (!res.ok) return false;
  const user = await res.json();
  return user?.email === ADMIN_EMAIL;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ ok: false, error: "method" }, 405);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ ok: false, error: "bad_request" }, 400);
  }
  // 앱에 넣을 공개 키 조회 (공개돼도 키를 만들 수 없음)
  if (body.action === "public_key") return json({ ok: true, public_key: (await keys()).pub });

  const mac = String(body.mac ?? "").trim().toUpperCase();
  if (!MAC_RE.test(mac)) return json({ ok: false, error: "bad_mac" }, 400);

  if (body.action === "activate") {
    // 코드 → PC 묶기/만료일 계산은 DB 함수(activate_code)가 한다. anon은 그 함수를 직접
    // 못 부르게 막아두고, 여기서 서비스 키로만 호출한다.
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/activate_code`, {
      method: "POST",
      headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ p_code: String(body.code ?? ""), p_mac: mac }),
    });
    if (!res.ok) return json({ ok: false, error: "server" }, 500);
    const r = await res.json();
    if (!r?.ok) return json({ ok: false, error: r?.error ?? "server" });
    return json({ ok: true, key: await makeKey(mac, r.expiry), expiry: r.expiry });
  }

  if (body.action === "issue") {
    if (!(await isAdmin(req.headers.get("Authorization")))) return json({ ok: false, error: "forbidden" }, 403);
    const days = Number(body.days);
    if (!Number.isInteger(days) || days < 1 || days > 3650) return json({ ok: false, error: "bad_days" }, 400);
    const expiry = expiryFromDays(days);
    return json({ ok: true, key: await makeKey(mac, expiry), expiry });
  }

  return json({ ok: false, error: "unknown_action" }, 400);
});
