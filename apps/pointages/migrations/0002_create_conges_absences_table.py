from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pointages", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS conges_absences (
                id BIGSERIAL PRIMARY KEY,
                type_absence VARCHAR(20) NOT NULL,
                date_debut DATE NOT NULL,
                date_fin DATE NOT NULL,
                statut VARCHAR(20) NOT NULL,
                motif TEXT NOT NULL DEFAULT '',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                employe_id BIGINT NOT NULL,
                approuve_par_id BIGINT NULL
            );
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS conges_absences;
            """,
        ),
    ]

