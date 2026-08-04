DROP TABLE IF EXISTS action;
DROP TABLE IF EXISTS session;

CREATE TABLE IF NOT EXISTS "action" (
	"action_id" INTEGER NOT NULL,
	"created_at" TIMESTAMP,
	"type" VARCHAR,
	"session_id" INTEGER NOT NULL,
	PRIMARY KEY("action_id")
);

CREATE TABLE IF NOT EXISTS "session" (
	"session_id" INTEGER NOT NULL,
	"seconds_duration" NUMERIC,
	"started_at" TIMESTAMP,
	"finish_at" TIMESTAMP,
	PRIMARY KEY("session_id"),
	FOREIGN KEY ("session_id") REFERENCES "action"("session_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
