create table public.datos_usuario(
  id serial NOT NULL,
  institucion_id integer not null,
  user_id integer not null,
  admin_institucion boolean not null,
  constraint datos_usuario_pkey PRIMARY KEY(id),
  CONSTRAINT datos_usuario_user_id_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT datos_usuario_institucion_id_fk_public_user_id FOREIGN KEY (institucion_id) REFERENCES public.institucion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

ALTER TABLE public.datos_usuario
  OWNER TO "Christian";
