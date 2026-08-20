/*
=====================================
HELPER FUNCTIONS
=====================================
*/


function parseCsv(text) {

    const rows = [];

    let row = [];
    let field = "";
    let insideQuotes = false;


    for (
        let i = 0;
        i < text.length;
        i++
    ) {

        const character =
            text[i];


        if (insideQuotes) {

            if (character === '"') {

                if (
                    text[i + 1] === '"'
                ) {

                    field += '"';

                    i++;

                }

                else {

                    insideQuotes = false;

                }

            }

            else {

                field += character;

            }

        }

        else {

            if (character === '"') {

                insideQuotes = true;

            }

            else if (
                character === ","
            ) {

                row.push(
                    field.trim()
                );

                field = "";

            }

            else if (
                character === "\n"
            ) {

                row.push(
                    field.trim()
                );


                if (
                    row.some(
                        value =>
                            value !== ""
                    )
                ) {

                    rows.push(
                        row
                    );

                }


                row = [];
                field = "";

            }

            else if (
                character === "\r"
            ) {

                // Ignore carriage return.

            }

            else {

                field += character;

            }

        }

    }


    if (insideQuotes) {

        throw new Error(
            "CSV contains an unclosed quoted field."
        );

    }


    row.push(
        field.trim()
    );


    if (
        row.some(
            value =>
                value !== ""
        )
    ) {

        rows.push(
            row
        );

    }


    return rows;

}


function percent(value) {

    return (
        value * 100
    ).toFixed(1) + "%";

}


function createPredictionRow(
    prediction,
    includeProbabilities = false
) {

    const row =
        document.createElement(
            "tr"
        );


    const reviewCell =
        document.createElement(
            "td"
        );

    reviewCell.textContent =
        prediction.review;


    const sentimentCell =
        document.createElement(
            "td"
        );

    sentimentCell.textContent =
        prediction.sentiment;


    const confidenceCell =
        document.createElement(
            "td"
        );

    confidenceCell.textContent =
        percent(
            prediction.confidence
        );


    row.appendChild(
        reviewCell
    );

    row.appendChild(
        sentimentCell
    );

    row.appendChild(
        confidenceCell
    );


    if (includeProbabilities) {

        const negativeCell =
            document.createElement(
                "td"
            );

        negativeCell.textContent =
            percent(
                prediction
                    .probabilities
                    .negative
            );


        const neutralCell =
            document.createElement(
                "td"
            );

        neutralCell.textContent =
            percent(
                prediction
                    .probabilities
                    .neutral
            );


        const positiveCell =
            document.createElement(
                "td"
            );

        positiveCell.textContent =
            percent(
                prediction
                    .probabilities
                    .positive
            );


        row.appendChild(
            negativeCell
        );

        row.appendChild(
            neutralCell
        );

        row.appendChild(
            positiveCell
        );

    }


    const uncertainCell =
        document.createElement(
            "td"
        );

    uncertainCell.textContent =
        prediction.is_uncertain
            ? "Yes"
            : "No";


    row.appendChild(
        uncertainCell
    );


    return row;

}


function buildSummary(
    predictions
) {

    let positive = 0;
    let neutral = 0;
    let negative = 0;
    let uncertain = 0;


    for (
        const prediction
        of predictions
    ) {

        if (
            prediction.sentiment
            === "positive"
        ) {

            positive++;

        }

        else if (
            prediction.sentiment
            === "neutral"
        ) {

            neutral++;

        }

        else if (
            prediction.sentiment
            === "negative"
        ) {

            negative++;

        }


        if (
            prediction.is_uncertain
        ) {

            uncertain++;

        }

    }


    return (
        `Total: ${predictions.length} | `
        + `Positive: ${positive} | `
        + `Neutral: ${neutral} | `
        + `Negative: ${negative} | `
        + `Uncertain: ${uncertain}`
    );

}


async function predictBatch(
    reviews
) {

    const response =
        await fetch(
            "/predict-batch",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        {
                            reviews: reviews
                        }
                    )
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail
            || "Batch prediction failed."
        );

    }


    return data.predictions;

}


/*
=====================================
SINGLE REVIEW
=====================================
*/


const button =
    document.getElementById(
        "analyze-button"
    );


button.addEventListener(
    "click",

    async function () {

        const review =
            document
                .getElementById(
                    "review"
                )
                .value
                .trim();


        const errorElement =
            document.getElementById(
                "error"
            );


        const resultElement =
            document.getElementById(
                "result"
            );


        errorElement.textContent =
            "";

        resultElement.style.display =
            "none";


        if (!review) {

            errorElement.textContent =
                "Please enter a review.";

            return;

        }


        try {

            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                {
                                    review: review
                                }
                            )
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail
                    || "Prediction failed."
                );

            }


            document
                .getElementById(
                    "sentiment"
                )
                .textContent =
                    data.sentiment;


            document
                .getElementById(
                    "confidence"
                )
                .textContent =
                    percent(
                        data.confidence
                    );


            document
                .getElementById(
                    "confidence-level"
                )
                .textContent =
                    data.confidence_level;


            document
                .getElementById(
                    "negative"
                )
                .textContent =
                    percent(
                        data
                            .probabilities
                            .negative
                    );


            document
                .getElementById(
                    "neutral"
                )
                .textContent =
                    percent(
                        data
                            .probabilities
                            .neutral
                    );


            document
                .getElementById(
                    "positive"
                )
                .textContent =
                    percent(
                        data
                            .probabilities
                            .positive
                    );


            document
                .getElementById(
                    "uncertain"
                )
                .textContent =
                    data.is_uncertain
                        ? "Yes"
                        : "No";


            resultElement.style.display =
                "block";

        }

        catch (error) {

            errorElement.textContent =
                error.message;

        }

    }
);


/*
=====================================
MANUAL BATCH
=====================================
*/


const batchButton =
    document.getElementById(
        "batch-button"
    );


batchButton.addEventListener(
    "click",

    async function () {

        const batchText =
            document
                .getElementById(
                    "batch-reviews"
                )
                .value
                .trim();


        const batchError =
            document.getElementById(
                "batch-error"
            );


        const batchResults =
            document.getElementById(
                "batch-results"
            );


        const tableBody =
            document.getElementById(
                "batch-table-body"
            );


        const summary =
            document.getElementById(
                "batch-summary"
            );


        batchError.textContent =
            "";

        batchResults.style.display =
            "none";

        tableBody.innerHTML =
            "";


        if (!batchText) {

            batchError.textContent =
                "Please enter at least one review.";

            return;

        }


        const reviews =
            batchText
                .split("\n")
                .map(
                    review =>
                        review.trim()
                )
                .filter(
                    review =>
                        review.length > 0
                );


        try {

            const predictions =
                await predictBatch(
                    reviews
                );


            for (
                const prediction
                of predictions
            ) {

                tableBody.appendChild(
                    createPredictionRow(
                        prediction
                    )
                );

            }


            summary.textContent =
                buildSummary(
                    predictions
                );


            batchResults.style.display =
                "block";

        }

        catch (error) {

            batchError.textContent =
                error.message;

        }

    }
);


/*
=====================================
CSV ANALYSIS
=====================================
*/


let latestCsvPredictions =
    [];


const csvButton =
    document.getElementById(
        "csv-button"
    );


const downloadButton =
    document.getElementById(
        "download-button"
    );


csvButton.addEventListener(
    "click",

    async function () {

        const fileInput =
            document.getElementById(
                "csv-file"
            );


        const csvError =
            document.getElementById(
                "csv-error"
            );


        const csvResults =
            document.getElementById(
                "csv-results"
            );


        const csvTableBody =
            document.getElementById(
                "csv-table-body"
            );


        const csvSummary =
            document.getElementById(
                "csv-summary"
            );


        csvError.textContent =
            "";

        csvResults.style.display =
            "none";

        downloadButton.style.display =
            "none";

        csvTableBody.innerHTML =
            "";

        latestCsvPredictions =
            [];


        if (
            fileInput.files.length
            === 0
        ) {

            csvError.textContent =
                "Please choose a CSV file.";

            return;

        }


        const file =
            fileInput.files[0];


        try {

            const text =
                await file.text();


            const rows =
                parseCsv(
                    text
                );


            if (
                rows.length < 2
            ) {

                throw new Error(
                    "CSV must contain a header and at least one review."
                );

            }


            const headers =
                rows[0]
                    .map(
                        header =>
                            header
                                .trim()
                                .toLowerCase()
                    );


            const reviewIndex =
                headers.indexOf(
                    "review"
                );


            if (
                reviewIndex === -1
            ) {

                throw new Error(
                    'CSV must contain a column named "review".'
                );

            }


            const reviews =
                [];


            for (
                let i = 1;
                i < rows.length;
                i++
            ) {

                const review =
                    rows[i][
                        reviewIndex
                    ]?.trim();


                if (review) {

                    reviews.push(
                        review
                    );

                }

            }


            if (
                reviews.length === 0
            ) {

                throw new Error(
                    "No valid reviews were found in the CSV."
                );

            }


            const predictions =
                await predictBatch(
                    reviews
                );


            latestCsvPredictions =
                predictions;


            for (
                const prediction
                of predictions
            ) {

                csvTableBody.appendChild(
                    createPredictionRow(
                        prediction,
                        true
                    )
                );

            }


            csvSummary.textContent =
                buildSummary(
                    predictions
                );


            csvResults.style.display =
                "block";


            downloadButton.style.display =
                "inline-block";

        }

        catch (error) {

            csvError.textContent =
                error.message;

        }

    }
);


/*
=====================================
DOWNLOAD CSV RESULTS
=====================================
*/


downloadButton.addEventListener(
    "click",

    function () {

        if (
            latestCsvPredictions.length
            === 0
        ) {

            return;

        }


        const rows = [

            [
                "review",
                "sentiment",
                "confidence",
                "confidence_level",
                "negative_probability",
                "neutral_probability",
                "positive_probability",
                "prediction_margin",
                "is_uncertain"
            ]

        ];


        for (
            const prediction
            of latestCsvPredictions
        ) {

            rows.push(
                [
                    prediction.review,
                    prediction.sentiment,
                    prediction.confidence,
                    prediction.confidence_level,
                    prediction
                        .probabilities
                        .negative,
                    prediction
                        .probabilities
                        .neutral,
                    prediction
                        .probabilities
                        .positive,
                    prediction.prediction_margin,
                    prediction.is_uncertain
                ]
            );

        }


        const csvContent =
            rows
                .map(
                    row =>
                        row
                            .map(
                                value => {

                                    const escaped =
                                        String(value)
                                            .replace(
                                                /"/g,
                                                '""'
                                            );


                                    return (
                                        `"${escaped}"`
                                    );

                                }
                            )
                            .join(",")
                )
                .join("\n");


        const blob =
            new Blob(
                [
                    csvContent
                ],
                {
                    type:
                        "text/csv;charset=utf-8;"
                }
            );


        const url =
            URL.createObjectURL(
                blob
            );


        const link =
            document.createElement(
                "a"
            );


        link.href =
            url;

        link.download =
            "sentiment_predictions.csv";


        document.body.appendChild(
            link
        );


        link.click();


        document.body.removeChild(
            link
        );


        URL.revokeObjectURL(
            url
        );

    }
);