from pathlib import Path


FRONTEND_URL = "http://localhost:5173"


def test_homepage_loads(page):
    """
    The React application should load successfully
    in a real Chromium browser.
    """

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    assert page.get_by_text(
        "Sentiment Intelligence",
        exact=True,
    ).is_visible()

    assert page.get_by_text(
        "Model online",
        exact=True,
    ).is_visible()


def test_single_review_flow(page):
    """
    A user should be able to submit one review
    and receive sentiment analysis.
    """

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    review_box = page.locator("textarea").first

    review_box.fill(
        "Amazing app, I absolutely love it."
    )

    page.get_by_role(
        "button",
        name="Analyze sentiment",
        exact=True,
    ).click()

    # Wait for a result element that only appears
    # after prediction succeeds.
    page.get_by_text(
        "Prediction margin",
        exact=False,
    ).wait_for(
        state="visible"
    )

    body_text = page.locator("body").inner_text()

    assert "confidence" in body_text.lower()
    assert "prediction margin" in body_text.lower()
    assert "uncertain" in body_text.lower()

    assert any(
        sentiment in body_text.lower()
        for sentiment in [
            "positive",
            "neutral",
            "negative",
        ]
    )


def test_batch_review_flow(page):
    """
    A user should be able to analyze several
    reviews through Batch Intelligence.
    """

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    page.get_by_text(
        "Batch Intelligence",
        exact=True,
    ).click()

    # Wait until the Batch Intelligence panel
    # has actually finished rendering.
    batch_button = page.get_by_role(
        "button",
        name="Analyze batch",
        exact=True,
    )

    batch_button.wait_for(
        state="visible"
    )

    review_box = page.locator(
        "textarea:visible"
    ).first

    review_box.wait_for(
        state="visible"
    )

    review_box.fill(
        (
            "Amazing app, I absolutely love it.\n"
            "The app crashes every time.\n"
            "It works fine, nothing special."
        )
    )

    assert batch_button.is_enabled()

    batch_button.click()

    page.get_by_text(
        "3 reviews analyzed",
        exact=False,
    ).wait_for(
        state="visible"
    )

    body_text = page.locator(
        "body"
    ).inner_text()

    assert "positive" in body_text.lower()
    assert "neutral" in body_text.lower()
    assert "negative" in body_text.lower()
    assert "uncertain" in body_text.lower()

    assert (
        "Amazing app, I absolutely love it."
        in body_text
    )

    assert (
        "The app crashes every time."
        in body_text
    )

    assert (
        "It works fine, nothing special."
        in body_text
    )
    
def test_csv_upload_flow(page, tmp_path):
    """
    A user should be able to upload a CSV
    and analyze all reviews.
    """

    csv_file = tmp_path / "reviews.csv"

    csv_file.write_text(
        (
            "review,rating\n"
            "\"Amazing app, I love it.\",5\n"
            "\"The app crashes constantly.\",1\n"
            "\"It works fine, nothing special.\",3\n"
        ),
        encoding="utf-8",
    )

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    page.get_by_text(
        "CSV Workspace",
        exact=True,
    ).click()

    file_input = page.locator(
        'input[type="file"]'
    )

    file_input.set_input_files(
        str(csv_file)
    )

    # We know from the failure output that
    # this exact button exists.
    page.get_by_role(
        "button",
        name="Analyze CSV",
        exact=True,
    ).click()

    page.get_by_text(
        "Review explorer",
        exact=True,
    ).wait_for(
        state="visible"
    )

    body_text = page.locator("body").inner_text()

    assert "3 reviews analyzed" in body_text.lower()

    assert (
        "Amazing app, I love it."
        in body_text
    )

    assert (
        "The app crashes constantly."
        in body_text
    )

    assert (
        "It works fine, nothing special."
        in body_text
    )


def test_csv_parser_preserves_commas(
    page,
    tmp_path,
):
    """
    A quoted comma must stay inside the
    review instead of creating a new column.
    """

    csv_file = (
        tmp_path
        / "quoted_reviews.csv"
    )

    expected_review = (
        "Amazing app, I absolutely love it."
    )

    csv_file.write_text(
        (
            "review,rating\n"
            "\"Amazing app, I absolutely love it.\",5\n"
        ),
        encoding="utf-8",
    )

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    page.get_by_text(
        "CSV Workspace",
        exact=True,
    ).click()

    page.locator(
        'input[type="file"]'
    ).set_input_files(
        str(csv_file)
    )

    page.get_by_role(
        "button",
        name="Analyze CSV",
        exact=True,
    ).click()

    page.get_by_text(
        "Review explorer",
        exact=True,
    ).wait_for(
        state="visible"
    )

    body_text = page.locator("body").inner_text()

    assert expected_review in body_text


def test_csv_download_button_appears(
    page,
    tmp_path,
):
    """
    CSV analysis should expose a prediction
    download control after completion.
    """

    csv_file = (
        tmp_path
        / "reviews.csv"
    )

    csv_file.write_text(
        (
            "review\n"
            "Amazing app\n"
        ),
        encoding="utf-8",
    )

    page.goto(FRONTEND_URL)

    page.wait_for_load_state("networkidle")

    page.get_by_text(
        "CSV Workspace",
        exact=True,
    ).click()

    page.locator(
        'input[type="file"]'
    ).set_input_files(
        str(csv_file)
    )

    page.get_by_role(
        "button",
        name="Analyze CSV",
        exact=True,
    ).click()

    page.get_by_text(
        "Review explorer",
        exact=True,
    ).wait_for(
        state="visible"
    )

    download_button = page.get_by_role(
        "button",
        name="Download",
        exact=False,
    )

    assert download_button.is_visible()