-- AIBlogBot 관리자 페이지용 테이블 생성 + 보안 정책
-- Supabase SQL Editor에서 그대로 실행하면 됩니다.

-- 1. 신청 내역 테이블 (홈페이지 "신청하기" 폼)
create table applications (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  name text not null,
  contact_type text not null,
  contact_value text not null,
  industry text not null,
  payment_method text not null,
  question text,
  status text not null default '신규'
);

-- 2. 라이선스 발급 이력 테이블
create table licenses (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  customer_name text not null,
  contact_value text,
  mac_address text not null,
  license_key text not null,
  period_months integer,
  issued_at date not null default current_date,
  expires_at date
);

-- 3. 보안 정책 활성화 (RLS)
alter table applications enable row level security;
alter table licenses enable row level security;

-- 4. 누구나(비회원) 신청서는 등록할 수 있지만, 조회는 못 하게
create policy "anyone_can_submit_application"
  on applications for insert
  to anon
  with check (true);

-- 5. 딱 대표님 계정(YOUR_ADMIN_EMAIL_HERE)만 조회/수정 가능
--    "authenticated"만 체크하면 회원가입만 하면 아무나 데이터를 볼 수 있으므로,
--    반드시 이메일까지 특정해서 잠가야 한다.
create policy "admin_only_read_applications"
  on applications for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_update_applications"
  on applications for update
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_read_licenses"
  on licenses for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_write_licenses"
  on licenses for insert
  to authenticated
  with check (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_update_licenses"
  on licenses for update
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

-- 6. 삭제 권한 (테스트 데이터 정리용)
create policy "admin_only_delete_applications"
  on applications for delete
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_delete_licenses"
  on licenses for delete
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

-- 7. 무료체험 사용 현황 테이블 (관리자 페이지에서 "몇 명이 몇 회 썼는지" 확인용)
--    MAC 주소 1개당 1행. 앱이 체험 1회를 실제로 소진할 때마다 report_trial_usage()를
--    호출해서 runs_used를 1씩 올린다.
create table trial_usage (
  id uuid primary key default gen_random_uuid(),
  mac_address text not null unique,
  runs_used integer not null default 0,
  first_used_at timestamptz not null default now(),
  last_used_at timestamptz not null default now()
);

alter table trial_usage enable row level security;

-- 8. 앱(anon)이 테이블에 직접 쓰지 못하게 막고, 아래 RPC 함수를 통해서만 기록하게 한다.
--    SECURITY DEFINER로 RLS를 우회해 upsert(없으면 생성/있으면 +1)를 안전하게 수행한다.
--    앱이 할 수 있는 건 "이 MAC 사용횟수 1 늘리기" 뿐이고, 조회/삭제는 여전히 불가능하다.
create or replace function report_trial_usage(p_mac text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into trial_usage (mac_address, runs_used, first_used_at, last_used_at)
  values (p_mac, 1, now(), now())
  on conflict (mac_address)
  do update set runs_used = trial_usage.runs_used + 1, last_used_at = now();
end;
$$;

grant execute on function report_trial_usage(text) to anon;

-- 8-1. (2026-09-27) 앱이 "이 PC가 체험을 몇 번 썼는지"만 조회할 수 있게 한다.
--      로컬 숨김 파일을 지워 체험을 리셋하는 걸 막기 위함. 알고 있는 MAC 하나의
--      숫자만 돌려주고, 테이블 전체 조회는 여전히 관리자만 가능.
create or replace function get_trial_runs(p_mac text)
returns integer
language sql
stable
security definer
set search_path = public
as $$
  select coalesce((select runs_used from trial_usage where mac_address = p_mac), 0)
$$;

grant execute on function get_trial_runs(text) to anon;

-- 9. 조회는 다른 테이블들과 동일하게 딱 대표님 계정만 가능
create policy "admin_only_read_trial_usage"
  on trial_usage for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

-- 10. 판매 채널 구분 (2026-07-31: 크몽 등 외부 채널 판매를 관리자 페이지에서
--     수동 기록할 때, 홈페이지 신청 건과 구분하기 위해 추가)
alter table licenses add column if not exists channel text not null default '홈페이지';

-- 11. 오류 로그 테이블 (2026-08-08: 고객마다 "안 돼요" 스크린샷을 매번 받지 않고도
--     원격으로 어떤 고객이 어느 단계에서 무슨 오류를 겪었는지 확인하기 위해 추가.
--     trial_usage/report_trial_usage와 동일한 구조 — 앱(anon)은 RPC로 기록만 가능,
--     조회는 관리자 계정만 가능.
create table error_logs (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  mac_address text not null,
  app_version text,
  context text,
  error_message text
);

alter table error_logs enable row level security;

create or replace function report_error_log(p_mac text, p_version text, p_context text, p_message text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into error_logs (mac_address, app_version, context, error_message)
  values (p_mac, p_version, p_context, p_message);
end;
$$;

grant execute on function report_error_log(text, text, text, text) to anon;

create policy "admin_only_read_error_logs"
  on error_logs for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

create policy "admin_only_delete_error_logs"
  on error_logs for delete
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

-- 12. 활성화 코드 (2026-09-27: 결제 고객에게 PC 고유번호를 따로 받지 않고
--     "ACT-XXXX-XXXX" 코드 하나만 보내면, 고객 앱이 처음 등록한 PC에 자동으로 묶는다.
--     이용 기간은 고객이 코드를 등록한 날부터 계산. 같은 PC 재설치 시 같은 만료일로
--     재등록 가능, 다른 PC에서는 거부. 등록되는 순간 licenses 이력에도 자동 기록.)
create table if not exists activation_codes (
  code text primary key,
  period_days integer not null,
  customer_name text,
  contact_value text,
  channel text default '홈페이지',
  application_id uuid,
  created_at timestamptz default now(),
  mac_address text,
  activated_at timestamptz,
  expires_on date
);

alter table activation_codes enable row level security;

create policy "admin_all_activation_codes"
  on activation_codes for all
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE')
  with check (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');

-- 앱(anon)은 코드 등록 RPC만 호출 가능. 결과로 만료일(YYMMDD)만 받아서 앱이 기존
-- PREM 키를 스스로 만들어 저장한다 (그 뒤로는 기존처럼 오프라인 검증).
create or replace function activate_code(p_code text, p_mac text)
returns json
language plpgsql
security definer
set search_path = public
as $$
declare
  r activation_codes;
  v_exp date;
begin
  select * into r from activation_codes where code = upper(trim(p_code)) for update;
  if not found then
    return json_build_object('ok', false, 'error', 'not_found');
  end if;
  if r.mac_address is not null and r.mac_address <> upper(trim(p_mac)) then
    return json_build_object('ok', false, 'error', 'used_elsewhere');
  end if;
  if r.mac_address is null then
    v_exp := (now() at time zone 'Asia/Seoul')::date + r.period_days;
    update activation_codes
      set mac_address = upper(trim(p_mac)), activated_at = now(), expires_on = v_exp
      where code = r.code;
    insert into licenses (customer_name, contact_value, channel, mac_address, license_key,
                          period_months, issued_at, expires_at)
    values (coalesce(r.customer_name, '활성화코드'), r.contact_value, coalesce(r.channel, '홈페이지'),
            upper(trim(p_mac)), r.code,
            case when r.period_days <= 1 then 0 else round(r.period_days / 30.0) end,
            (now() at time zone 'Asia/Seoul')::date, v_exp);
  else
    v_exp := r.expires_on;
  end if;
  return json_build_object('ok', true, 'expiry', to_char(v_exp, 'YYMMDD'));
end;
$$;

grant execute on function activate_code(text, text) to anon;

-- 13. (2026-09-27) 서버 서명 키 전환. activate_code는 이제 Edge Function "license"가
--     서비스 키로만 호출한다 (앱이 직접 부르면 만료일만 받아 예전 SALT 방식 키를 만들 수
--     있었으므로 anon 권한 회수). 예전 방식(PREM-) 키는 발급 기록이 있는 것만 인정하는데,
--     앱에 내장된 목록 이후에 기록된 키를 확인하기 위한 조회 함수 추가.
revoke execute on function activate_code(text, text) from anon, authenticated, public;

create or replace function is_registered_key(p_key text)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from licenses where upper(trim(license_key)) = upper(trim(p_key)))
$$;

grant execute on function is_registered_key(text) to anon;

-- 14. 서명 키 보관 표. Edge Function "license"가 처음 실행될 때 키를 스스로 만들어 저장한다.
--     RLS만 켜고 정책을 하나도 안 만들어서 anon/관리자 로그인으로도 읽을 수 없고,
--     서비스 키(Edge Function 안에서만 쓰임)로만 접근 가능.
create table if not exists license_signing_keys (
  id integer primary key check (id = 1),
  private_pkcs8 text not null,
  public_raw text not null,
  created_at timestamptz default now()
);
alter table license_signing_keys enable row level security;
revoke all on license_signing_keys from anon, authenticated;

-- 15. 사용 기록 (2026-09-29: 스마트상점 분기별 활용도 점검·초기창업패키지 근거·미사용 고객 관리용).
--     발행 1건마다 앱이 report_usage()로 기록, 관리자는 usage_summary 뷰로 PC별 요약 조회.
-- 1. 발행 1건마다 한 줄씩 쌓이는 표
create table if not exists usage_logs (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  mac_address text not null,
  app_version text,
  license_mode text,   -- TRIAL / PAID / PERMANENT
  result text          -- success / failed
);

alter table usage_logs enable row level security;
create index if not exists usage_logs_mac_created_idx on usage_logs (mac_address, created_at desc);

-- 2. 앱(anon)은 이 함수로 기록만 할 수 있다 (조회 불가). 값 길이를 잘라 이상한 입력이 쌓이지 않게 한다.
create or replace function report_usage(p_mac text, p_version text, p_mode text, p_result text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_mac is null or length(p_mac) = 0 then
    return;
  end if;
  insert into usage_logs (mac_address, app_version, license_mode, result)
  values (left(p_mac, 64), left(p_version, 20), left(p_mode, 20),
          case when p_result in ('success', 'failed') then p_result else 'failed' end);
end;
$$;

grant execute on function report_usage(text, text, text, text) to anon;

-- 3. 조회는 관리자 계정만 — 이메일은 이미 운영 중인 error_logs 규칙에서 그대로 가져온다.
do $$
declare q text;
begin
  select qual into q from pg_policies
   where tablename = 'error_logs' and policyname = 'admin_only_read_error_logs';
  if q is null then
    raise exception 'error_logs 관리자 규칙을 찾지 못했습니다';
  end if;
  execute 'drop policy if exists "admin_only_read_usage_logs" on usage_logs';
  execute format('create policy "admin_only_read_usage_logs" on usage_logs for select to authenticated using (%s)', q);
end $$;

-- 4. 관리자 페이지용 PC별 요약. security_invoker라 위 관리자 규칙이 그대로 적용된다.
create or replace view usage_summary with (security_invoker = true) as
select
  mac_address,
  max(created_at) filter (where result = 'success') as last_success_at,
  count(*) filter (where result = 'success' and created_at > now() - interval '30 days') as success_30d,
  count(*) filter (where result = 'success' and created_at >= date_trunc('quarter', now())) as success_quarter,
  count(*) filter (where result = 'success') as success_total,
  count(*) filter (where result = 'failed' and created_at > now() - interval '30 days') as failed_30d
from usage_logs
group by mac_address;


-- 16. 광고성 정보 수신 동의 (2026-09-29): 신청서 선택 체크(기본 해제). true인 신청자에게만 광고성 문자·카톡 발송.
alter table applications add column if not exists marketing_consent boolean not null default false;
