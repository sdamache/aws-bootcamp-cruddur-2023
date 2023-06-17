-- this file was manually created
INSERT INTO public.users (display_name, email,handle, cognito_user_id)
VALUES
  ('Sdamache', 'sdamache@asu.edu','sdamache' ,'MOCK'),
  ('Sai Nikhl', 'nikhild.sai@gmail.com','nikhildsai' ,'MOCK');
  ('Londo Mollari', 'lmollari@centari.com', 'londo', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'nikhildsai' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )