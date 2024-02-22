import csv
import sys
import gzip
import click
import shutil
import casanova
import fasttext

from preprocess import lead_paragraph, title_lead

# Remove warning
fasttext.FastText.eprint = lambda x: None

@click.command()
@click.option("--model", default='FASTTEXT-MODEL-ROUND-2.model.gz')
@click.argument("input_csv",  type=click.Path(readable=True))
@click.argument("output_csv", type=click.Path(writable=True))
def predict(input_csv, output_csv, model):
    """Enrich input file with prediction from model"""

    # Unzip model file
    with gzip.open(model, 'rb') as f_in:
        with open('FASTTEXT-MODEL-ROUND-2-UNZIP.model', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Load FastText model
    model_unzip = fasttext.load_model('FASTTEXT-MODEL-ROUND-2-UNZIP.model')

    # Enrich input file with prediction
    with open(input_csv) as input_file, \
        open(output_csv, 'w') as output_file:

        enricher = casanova.enricher(
            input_file,
            output_file,
            add=["title_lead", "prediction_on_title_lead", "confidence"]
        )

        if enricher.headers:
            title_pos = enricher.headers.title
            content_pos = enricher.headers.content

        else:
            click.echo("input_csv is not a valid csv file.")

        csv.field_size_limit(sys.maxsize)

        for row in enricher:

            lead = lead_paragraph(row[content_pos])
            title_and_lead = title_lead(row[title_pos], lead)

            model_output = model_unzip.predict(title_and_lead)
            prediction = model_output[0][0].strip("__label__")
            confidence = model_output[1][0]

            enricher.writerow(row, [title_and_lead, prediction, confidence])

if __name__ == '__main__':
    predict()