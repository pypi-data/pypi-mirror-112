"""Adds zone_start to tags

Revision ID: 5eae6a0253f5
Revises: 9581ffb09767
Create Date: 2021-04-29 10:58:04.477074

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '5eae6a0253f5'
down_revision = '9581ffb09767'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE tags ADD COLUMN zone_start timestamp without time zone "
        "DEFAULT (now() at time zone 'UTC')")
    op.execute("DROP FUNCTION append_history CASCADE")
    op.execute("""CREATE FUNCTION append_history()
        RETURNS TRIGGER
        LANGUAGE plpgsql
    AS
    $$
    DECLARE
        curr_hist          history%ROWTYPE;
        prev_hist          history%ROWTYPE;
        min_time           interval;
        min_time_returning interval;
        tag_returning      boolean := FALSE;
    BEGIN
        -- RAISE NOTICE 'In append_history():';
        -- RAISE NOTICE 'New Zone = %', NEW.zone_id;
        -- Fetch the last complete history entry for this tag
        SELECT * INTO prev_hist FROM history WHERE tag_id = OLD.id AND end_ts IS NOT NULL ORDER BY end_ts DESC LIMIT 1;
        IF FOUND THEN
            -- RAISE NOTICE 'Previous Zone = %', prev_hist.zone_id;
            IF prev_hist.zone_id = NEW.zone_id THEN
                -- We are trying to return to the previous zone, apply extra hysteresis
                -- RAISE NOTICE 'Returning';
                tag_returning := TRUE;
            END IF;
        END IF;

        -- Fetch current open history entry
        SELECT * INTO curr_hist FROM history WHERE tag_id = OLD.id AND end_ts IS NULL;
        IF FOUND THEN
            DECLARE
                duration_curr interval;
            BEGIN
                SELECT CONCAT(value, 'sec')::interval INTO min_time from settings WHERE name = 'MIN_SEC_IN_LOCATION';
                SELECT CONCAT(value, 'sec')::interval
                INTO min_time_returning
                FROM settings
                WHERE name = 'MIN_SEC_IN_LOCATION_IF_RETURNING';
                SELECT (now() at time zone 'utc') - curr_hist.start_ts INTO duration_curr;
                -- RAISE NOTICE 'Current Zone = %, duration = %', OLD.zone_id, duration_curr;
                -- IF tag_returning THEN
                --     RAISE NOTICE '% < % = %', duration_curr, min_time_returning, duration_curr < min_time_returning;
                -- ELSE
                --     RAISE NOTICE '% < % = %', duration_curr, min_time, duration_curr < min_time;
                -- END IF;
                IF (tag_returning = TRUE AND duration_curr < min_time_returning) OR
                   (tag_returning = FALSE AND duration_curr < min_time) THEN
                    -- We didn't stay here long enough, extend the previous history entry and delete current
                    -- RAISE NOTICE 'Hit';
                    UPDATE history SET end_ts = NULL WHERE id = prev_hist.id;
                    DELETE FROM history WHERE id = curr_hist.id;
                    IF tag_returning = TRUE THEN
                        -- Just re-open the previous history entry if returning otherwise we rely on the
                        -- code below to close out the previous entry and add the new one
                        -- RAISE NOTICE 'Returning hit';
                        UPDATE tags SET zone_start = prev_hist.start_ts WHERE id = NEW.id;
                        return NEW;
                    END IF;
                END IF;
            END;
        END IF;

        --RAISE NOTICE 'Pass through';
        UPDATE history SET end_ts = (now() at time zone 'utc') WHERE tag_id = OLD.id AND end_ts IS NULL;
        INSERT INTO history (tag_id, zone_id, distance, zone_name)
        VALUES (NEW.id, NEW.zone_id, NEW.distance,
                (SELECT zones.name from zones where zones.id = NEW.zone_id));
        UPDATE tags SET zone_start = (now() at time zone 'utc') WHERE id = NEW.id;
        RETURN NEW;
    END;
    $$""")  # noqa: E501
    op.execute("""CREATE TRIGGER tags_update_zone
                AFTER UPDATE OF zone_id ON tags FOR EACH ROW
                WHEN (OLD.zone_id IS DISTINCT FROM NEW.zone_id)
                EXECUTE PROCEDURE append_history();""")


def downgrade():
    op.execute("ALTER TABLE tags DROP COLUMN zone_start")
    op.execute("DROP FUNCTION append_history CASCADE")
    op.execute("""CREATE FUNCTION append_history()
        RETURNS TRIGGER
        LANGUAGE plpgsql
    AS
    $$
    DECLARE
        curr_hist          history%ROWTYPE;
        prev_hist          history%ROWTYPE;
        min_time           interval;
        min_time_returning interval;
        tag_returning      boolean := FALSE;
    BEGIN
        -- RAISE NOTICE 'In append_history():';
        -- RAISE NOTICE 'New Zone = %', NEW.zone_id;
        -- Fetch the last complete history entry for this tag
        SELECT * INTO prev_hist FROM history WHERE tag_id = OLD.id AND end_ts IS NOT NULL ORDER BY end_ts DESC LIMIT 1;
        IF FOUND THEN
            -- RAISE NOTICE 'Previous Zone = %', prev_hist.zone_id;
            IF prev_hist.zone_id = NEW.zone_id THEN
                -- We are trying to return to the previous zone, apply extra hysteresis
                -- RAISE NOTICE 'Returning';
                tag_returning := TRUE;
            END IF;
        END IF;

        -- Fetch current open history entry
        SELECT * INTO curr_hist FROM history WHERE tag_id = OLD.id AND end_ts IS NULL;
        IF FOUND THEN
            DECLARE
                duration_curr interval;
            BEGIN
                SELECT CONCAT(value, 'sec')::interval INTO min_time from settings WHERE name = 'MIN_SEC_IN_LOCATION';
                SELECT CONCAT(value, 'sec')::interval
                INTO min_time_returning
                FROM settings
                WHERE name = 'MIN_SEC_IN_LOCATION_IF_RETURNING';
                SELECT (now() at time zone 'utc') - curr_hist.start_ts INTO duration_curr;
                -- RAISE NOTICE 'Current Zone = %, duration = %', OLD.zone_id, duration_curr;
                -- IF tag_returning THEN
                --     RAISE NOTICE '% < % = %', duration_curr, min_time_returning, duration_curr < min_time_returning;
                -- ELSE
                --     RAISE NOTICE '% < % = %', duration_curr, min_time, duration_curr < min_time;
                -- END IF;
                IF (tag_returning = TRUE AND duration_curr < min_time_returning) OR
                   (tag_returning = FALSE AND duration_curr < min_time) THEN
                    -- We didn't stay here long enough, extend the previous history entry and delete current
                    -- RAISE NOTICE 'Hit';
                    UPDATE history SET end_ts = NULL WHERE id = prev_hist.id;
                    DELETE FROM history WHERE id = curr_hist.id;
                    IF tag_returning = TRUE THEN
                        -- Just re-open the previous history entry if returning otherwise we rely on the
                        -- code below to close out the previous entry and add the new one
                        -- RAISE NOTICE 'Returning hit';
                        return NEW;
                    END IF;
                END IF;
            END;
        END IF;

        --RAISE NOTICE 'Pass through';
        UPDATE history SET end_ts = (now() at time zone 'utc') WHERE tag_id = OLD.id AND end_ts IS NULL;
        INSERT INTO history (tag_id, zone_id, distance, zone_name)
        VALUES (NEW.id, NEW.zone_id, NEW.distance,
                (SELECT zones.name from zones where zones.id = NEW.zone_id));
        RETURN NEW;
    END;
    $$""")  # noqa: E501
    op.execute("""CREATE TRIGGER tags_update_zone
                AFTER UPDATE OF zone_id ON tags FOR EACH ROW
                WHEN (OLD.zone_id IS DISTINCT FROM NEW.zone_id)
                EXECUTE PROCEDURE append_history();""")
