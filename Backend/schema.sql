-- Run this once in Supabase: SQL Editor -> New query -> paste -> Run
create table profiles(id uuid primary key references auth.users(id) on delete cascade,email text,name text,mobile text,role text not null default 'customer',created_at timestamptz default now());
create function public.handle_new_user() returns trigger language plpgsql security definer set search_path=public as $$
begin insert into public.profiles(id,email,name,mobile) values(new.id,new.email,new.raw_user_meta_data->>'name',new.raw_user_meta_data->>'mobile'); return new; end $$;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();
create table bookings(id text primary key,user_id uuid references auth.users(id) on delete set null,hotel text not null,cat text not null,rooms int[] not null,from_date date not null,to_date date not null,plan text not null,adults int,children int,guest_name text,mobile text not null,email text,address text,city text,pin text,requests text,total int not null,paid int not null default 0,status text not null default 'Pending',state text,hold_expires timestamptz,rz_order_id text,rz_payment_id text,created_at timestamptz default now());
create index on bookings(mobile); create index on bookings(user_id); create index on bookings(rz_order_id);
-- one row per room per night: the primary key makes double booking impossible
create table room_nights(hotel text,room int,night date,booking_id text references bookings(id) on delete cascade,primary key(hotel,room,night));
create table tickets(id text primary key,booking text,hotel text,created_at timestamptz default now());
alter table profiles enable row level security; alter table bookings enable row level security; alter table room_nights enable row level security; alter table tickets enable row level security;
create policy "own profile" on profiles for select using(auth.uid()=id);
create policy "own bookings" on bookings for select using(auth.uid()=user_id);
-- customers can edit only name and mobile (never their role)
revoke update on profiles from anon,authenticated; grant update(name,mobile) on profiles to authenticated;
create policy "edit own profile" on profiles for update using(auth.uid()=id);
-- make yourself the manager (after you sign up in the app):
-- update profiles set role='admin' where email='you@example.com';
