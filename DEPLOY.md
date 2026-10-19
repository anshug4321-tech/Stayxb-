# Deploy guide (Supabase + Render)
The FastAPI server also serves the website, so you get ONE link. Database + login = Supabase. Hosting = Render.

1. Supabase: create project -> SQL Editor -> run `backend/schema.sql`. Copy Project URL, anon key, service_role key. Authentication -> URL Configuration: set Site URL to your Render link (step 4, you can update it later).
2. Razorpay: OPTIONAL. Skip it: the app then uses free demo payment (no real money). Do not add RAZORPAY lines on Render.
3. GitHub: new repo, upload the contents of this folder.
4. Render: New -> Web Service -> your repo -> Root Directory `backend` -> Build `pip install -r requirements.txt` -> Start `uvicorn main:app --host 0.0.0.0 --port $PORT` -> add every line of `backend/.env.example` as Environment Variables (FRONTEND_ORIGIN = your Render link) and PYTHON_VERSION=3.11.9. Deploy.
5. Open your Render link: the app opens. Check /api/health too.
7. Manager: sign up in the app, then in Supabase SQL Editor: `update profiles set role='admin' where email='you@example.com';`

Notes: free Render sleeps when idle (first load ~30 s). Never share the service_role key, Razorpay secret or Anthropic key. Mobile-only booking lookup shows masked details; add SMS OTP for stronger privacy.
