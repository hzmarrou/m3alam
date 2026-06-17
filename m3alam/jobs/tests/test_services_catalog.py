from jobs.forms import JobRequestForm


def test_job_form_category_choices_match_services_list():
    form = JobRequestForm()
    values = [choice[0] for choice in form.fields["category"].choices]
    labels = [choice[1] for choice in form.fields["category"].choices]
    assert "ascenseurs" in values
    assert "plomberie" in values
    assert "vitrerie-aluminium" in values
    assert "Ascenseurs" in labels
    assert "Électricité" in labels
    assert "Vitrerie aluminium" in labels
    assert len(values) == 28
