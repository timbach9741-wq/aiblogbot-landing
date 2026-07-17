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

-- 5. 로그인한 관리자만 조회/수정 가능
create policy "admin_can_read_applications"
  on applications for select
  to authenticated
  using (true);

create policy "admin_can_update_applications"
  on applications for update
  to authenticated
  using (true);

create policy "admin_can_read_licenses"
  on licenses for select
  to authenticated
  using (true);

create policy "admin_can_write_licenses"
  on licenses for insert
  to authenticated
  with check (true);

create policy "admin_can_update_licenses"
  on licenses for update
  to authenticated
  using (true);
