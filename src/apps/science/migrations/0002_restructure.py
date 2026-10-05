# Понятные имена моделей/полей/таблиц научного сервиса; страница центра теперь может
# заполняться из админки (content), а старые свёрстанные шаблоны указываются явно.
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints, move_content_type

# Бывший pages/utils/aliases.scientific_center_name_to_page
LEGACY_TEMPLATES = {
    "Научный центр нейротехнологий и процессов управления": "neural_technologies.html",
    "Центр научно-технологической инициативы «Фотоника»": "photon.html",
    "Международный научно-исследовательский центр реставрации и сохранения архитектурного наследия": "restoration_architectural_heritage.html",
    "Научный центр комплексного исследования и эффективной разработки недр": "subsoil_development.html",
    "Научный центр техники и технологий строительства": "technology_and_building.html",
    "Научный центр транспортных систем и комплексов": "operational_systems_and_complexes.html",
    "Научный центр технологий машиностроения и приборостроения": "technologies_mechanical_engineering.html",
    "Международный центр трансфера технологий": "transfer-center.html",
}


def fill_legacy_templates(apps, schema_editor):
    ScientificCenter = apps.get_model("science", "ScientificCenter")
    for center in ScientificCenter.objects.all():
        template = LEGACY_TEMPLATES.get(" ".join((center.name or "").split()))
        if template:
            center.legacy_template = template
            center.save(update_fields=["legacy_template"])


class Migration(migrations.Migration):

    dependencies = [
        ("science", "0001_move_from_pages"),
        ("academy", "0002_restructure"),
    ]

    operations = [
        move_content_type("science", "scientificcenters", "science", "scientificcenter"),
        move_content_type("science", "equipmentdata", "science", "equipment"),
        move_content_type("science", "partnerdata", "science", "partner"),
        migrations.RenameModel("ScientificCenters", "ScientificCenter"),
        migrations.RenameModel("EquipmentData", "Equipment"),
        migrations.RenameModel("PartnerData", "Partner"),
        migrations.RenameField("scientificcenter", "faculty_field", "department"),
        migrations.RenameField("scientificcenter", "page_url", "slug"),
        migrations.RenameField("scientificcenter", "display", "is_published"),
        migrations.RenameField("scientificcenter", "email_fields", "emails"),
        migrations.AddField(
            model_name="scientificcenter",
            name="content",
            field=models.TextField(blank=True, default="", verbose_name="Подробное описание"),
        ),
        migrations.AddField(
            model_name="scientificcenter",
            name="legacy_template",
            field=models.CharField(blank=True, default="", max_length=100, verbose_name="Старый шаблон страницы"),
        ),
        immediate_constraints(),
        migrations.RunPython(fill_legacy_templates, migrations.RunPython.noop),
        migrations.AlterModelTable("scientificcenter", None),
        migrations.AlterModelTable("equipment", None),
        migrations.AlterModelTable("partner", None),
        migrations.AlterModelTable("scientificspecialty", None),
        migrations.AlterModelTable("dissertationcommittee", None),
    ]
