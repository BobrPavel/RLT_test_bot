--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2025-12-24 16:37:45

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 58604)
-- Name: video_snapshots; Type: TABLE; Schema: public; Owner: RLT_test_bot
--

CREATE TABLE public.video_snapshots (
    id uuid NOT NULL,
    video_id uuid NOT NULL,
    views_count integer NOT NULL,
    likes_count integer NOT NULL,
    reports_count integer NOT NULL,
    comments_count integer NOT NULL,
    delta_views_count integer NOT NULL,
    delta_likes_count integer NOT NULL,
    delta_reports_count integer NOT NULL,
    delta_comments_count integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.video_snapshots OWNER TO "RLT_test_bot";

--
-- TOC entry 215 (class 1259 OID 58599)
-- Name: videos; Type: TABLE; Schema: public; Owner: RLT_test_bot
--

CREATE TABLE public.videos (
    id uuid NOT NULL,
    video_created_at timestamp with time zone NOT NULL,
    views_count integer NOT NULL,
    likes_count integer NOT NULL,
    reports_count integer NOT NULL,
    comments_count integer NOT NULL,
    creator_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.videos OWNER TO "RLT_test_bot";

--
-- TOC entry 4640 (class 2606 OID 58608)
-- Name: video_snapshots video_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: RLT_test_bot
--

ALTER TABLE ONLY public.video_snapshots
    ADD CONSTRAINT video_snapshots_pkey PRIMARY KEY (id);


--
-- TOC entry 4638 (class 2606 OID 58603)
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: RLT_test_bot
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- TOC entry 4641 (class 2606 OID 58609)
-- Name: video_snapshots video_snapshots_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: RLT_test_bot
--

ALTER TABLE ONLY public.video_snapshots
    ADD CONSTRAINT video_snapshots_video_id_fkey FOREIGN KEY (video_id) REFERENCES public.videos(id) ON DELETE CASCADE;


-- Completed on 2025-12-24 16:37:46

--
-- PostgreSQL database dump complete
--

