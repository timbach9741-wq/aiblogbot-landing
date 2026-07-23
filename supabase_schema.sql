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

-- 9. 조회는 다른 테이블들과 동일하게 딱 대표님 계정만 가능
create policy "admin_only_read_trial_usage"
  on trial_usage for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'YOUR_ADMIN_EMAIL_HERE');
