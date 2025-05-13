from django.utils.translation import get_language
...
def profiles(request, id):
    profile_object = get_object_or_404(EmployeeProfile, pk=id)

    if get_language() == 'en' and profile_object.full_name_en:
        page_title = profile_object.full_name_en
    else:
        page_title = profile_object.full_name

    return render(
        request,
        "profile.html",
        {
            "title": page_title,
            "employee": model_to_dict(profile_object),
        },
    )
