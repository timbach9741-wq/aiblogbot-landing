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

-- 5. 딱 대표님 계정(timbach9741@gmail.com)만 조회/수정 가능
--    "authenticated"만 체크하면 회원가입만 하면 아무나 데이터를 볼 수 있으므로,
--    반드시 이메일까지 특정해서 잠가야 한다.
create policy "admin_only_read_applications"
  on applications for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

create policy "admin_only_update_applications"
  on applications for update
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

create policy "admin_only_read_licenses"
  on licenses for select
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

create policy "admin_only_write_licenses"
  on licenses for insert
  to authenticated
  with check (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

create policy "admin_only_update_licenses"
  on licenses for update
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

-- 6. 삭제 권한 (테스트 데이터 정리용)
create policy "admin_only_delete_applications"
  on applications for delete
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');

create policy "admin_only_delete_licenses"
  on licenses for delete
  to authenticated
  using (auth.jwt() ->> 'email' = 'timbach9741@gmail.com');
