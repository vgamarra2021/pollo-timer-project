DROP TABLE IF EXISTS action;
DROP TABLE IF EXISTS session;

CREATE TABLE "session" (
	"session_id" INTEGER NOT NULL,
	"seconds_duration" NUMERIC,
	"is_active" BOOLEAN,
	"started_at" DATETIME,
	"finish_at" DATETIME,
	PRIMARY KEY("session_id")
);

CREATE TABLE "action" (
	"action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"created_at" DATETIME,
	"type" VARCHAR,
	"session_id" INTEGER NOT NULL,
	FOREIGN KEY ("session_id") REFERENCES "session"("session_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
