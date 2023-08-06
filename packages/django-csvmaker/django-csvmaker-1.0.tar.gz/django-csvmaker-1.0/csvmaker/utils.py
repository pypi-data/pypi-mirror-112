import csv
from django.http import HttpResponse

def generate_csv_from_queryset(queryset, csv_name = "query_csv"):
    """
    Genera un file csv a partire da un oggetto di tipo QuerySet
    :param queryset: oggetto di tipo QuerySet
    :param csv_name: campo opzionale per indicare il nome di output del csv
    :return: oggetto response
    """
    try:
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=' + csv_name + '.csv'},
        )
        model_field_names = []
        writer = csv.writer(response, delimiter=';')
        for field in queryset.first()._meta.local_fields:
            model_field_names.append(field.name)
        writer.writerow(model_field_names)

        for query in queryset:
            csv_row = []
            for field in queryset.first()._meta.local_fields:
                csv_row.append(getattr(query, field.attname))
            writer.writerow(csv_row)

        return response
    except Exception as e:
        return e