"""JSON Viewing utilities.
"""
import pandas as pd
from typing import List, Dict, Optional, Any
from functools import partial
from .docs import DocUtilsMixin

class Viewer(DocUtilsMixin):
    @staticmethod
    def is_in_ipython():
        """
        Determines if current code is executed within an ipython session.
        """
        is_in_ipython = False
        # Check if the runtime is within an interactive environment, i.e., ipython.
        try:
            from IPython import get_ipython  # pylint: disable=import-error
            if get_ipython():
                is_in_ipython = True
        except ImportError:
            pass  # If dependencies are not available, then not interactive for sure.
        return is_in_ipython

    def is_in_notebook(self) -> bool:
        """
        Determines if current code is executed from an ipython notebook.
        """
        is_in_notebook = False
        if self.is_in_ipython():
            # The import and usage must be valid under the execution path.
            from IPython import get_ipython
            if 'IPKernelApp' in get_ipython().config:
                is_in_notebook = True
        return is_in_notebook

    def show_df(self, df: pd.DataFrame,
        image_fields: List[str]=[], audio_fields: List[str]=[],
        chunk_image_fields: List[str]=[], chunk_audio_fields: List[str]=[],
        image_width: int=60, include_vector: bool=False, return_html: bool=False):
            """
                Shows a dataframe with the images and audio included inside the dataframe.
                Args:
                    df:
                        Pandas DataFrame
                    image_fields:
                        List of fields with the images
                    audio_fields:
                        List of fields for the audio
                    nrows:
                        Number of rows to preview
                    image_width:
                        The width of the images
                    include_vector:
                        If True, includes the vector fields
            """
            render_image_with_width = partial(self.render_image_in_html, image_width=image_width)
            formatters = {image:render_image_with_width for image in image_fields}
            formatters.update({audio: self.render_audio_in_html for audio in audio_fields})
            formatters.update({chunk_image: self.render_image_chunk for chunk_image in chunk_image_fields})
            formatters.update({chunk_audio: self.render_audio_chunk for chunk_audio in chunk_audio_fields})
            if not include_vector:
                cols = [x for x in list(df.columns) if '_vector_' not in x]
                df = df[cols]
            try:
                if return_html:
                    return df.to_html(escape=False, formatters=formatters)
                from IPython.core.display import HTML
                return HTML(df.to_html(escape=False ,formatters=formatters))
            except ImportError:
                return df

    def render_image_in_html(self, path, image_width) -> str:
        """
        Render image in HTML
        """
        return '<img src="'+ path + f'" width="{image_width}" >'

    def render_audio_in_html(self, path) -> str:
        """
        Render the audio in HTML
        """
        return f"<audio controls><source src='{x}' type='audio/{self.get_audio_format(x)}'></audio>"

    def unnest_json(self, json_data: List[Dict], schema: List[str], chunk_schema: List[str], 
        missing_treatment="return_empty_string"):
        """
        Unnest the JSON
        """
        unnested_json = {}
        for k in schema:
            unnested_json[k] = self.get_field_across_documents(k, json_data, 
                missing_treatment=missing_treatment)
        # Check if any of the field is a list
        for chunk_f in chunk_schema:
            # get the chunk field - assume the chunk field is the last field
            if '.' in chunk_f:
                chunk_field = ''.join(f + '.' for f in chunk_f.split('.')[:-1])[:-1]
                data_field = chunk_f.split('.')[-1]
            else:
                chunk_field = chunk_f
                data_field = chunk_f
            if isinstance(self.get_field(chunk_field, json_data[0]), dict):
                all_chunk_data = self.get_field_across_documents(chunk_field, json_data, missing_treatment=missing_treatment)
                chunk_data = [self.get_field_across_documents(data_field, d, missing_treatment=missing_treatment) for d in all_chunk_data]
            else:
                chunk_data = self.get_field_across_documents(chunk_field, json_data, missing_treatment=missing_treatment)
            if '.' in chunk_f:
                unnested_json[chunk_field + '.' + data_field] = chunk_data
            else:
                unnested_json[chunk_field] = chunk_data
        if '_id' in json_data[0].keys():
            unnested_json['_id'] = self.get_field_across_documents('_id', json_data, missing_treatment=missing_treatment)
        return unnested_json

    @classmethod
    def _is_string_integer(cls, x):
        """Test if a string is numeric
        """
        try:
            int(x)
            return True
        except:
            return False

    def highlight(self, text1, text2):
        # Highlight text2 inside text1 in HTML
        return text1.replace(text2, '<mark>' + text2 + '</mark>')

    def show_json(self, json: dict, text_fields: List[str]=[], image_fields: List[str]=[],
        audio_fields: List[str]=[], chunk_image_fields: List[str]=[], chunk_audio_fields: List[str]=[],
        nrows: int=None, image_width: int=60, include_vector=False, return_html: bool=False, missing_treatment: str='return_empty_string',
        highlight_fields={}):
        """
        Function for showing the JSON field
        """
        fields_to_show = image_fields + audio_fields + text_fields 
        fields_to_get = fields_to_show + list(highlight_fields.keys())
        for x in highlight_fields.values():
            fields_to_get += x
        if text_fields is None:
            json = self.unnest_json(self.clean_results(json), schema=fields_to_get, chunk_schema= chunk_image_fields + chunk_audio_fields, missing_treatment=missing_treatment)
        else:
            json = self.unnest_json(self.clean_results(json), schema=fields_to_get, chunk_schema=chunk_image_fields + chunk_audio_fields, missing_treatment=missing_treatment)

        for field_to_highlight, highlight in highlight_fields.items():
            for h in highlight:
                highlighters = json[h]
                json[field_to_highlight] = [self.highlight(x, highlighters[i]) for i, x in enumerate(json[field_to_highlight])]
                if h not in fields_to_show:
                    del json[h]
        if nrows is not None:
            json = json[:nrows]
        if text_fields is None and len(image_fields) == 0 and len(audio_fields) == 0:
            return self.show_df(pd.DataFrame(json), image_fields=image_fields, audio_fields=audio_fields,
                chunk_image_fields=chunk_image_fields, chunk_audio_fields=chunk_audio_fields,
                image_width=image_width, include_vector=include_vector, return_html=return_html)
        return self.show_df(pd.DataFrame(json),
            image_fields=image_fields, audio_fields=audio_fields,
            chunk_image_fields=chunk_image_fields, chunk_audio_fields=chunk_audio_fields,
            image_width=image_width, include_vector=include_vector, return_html=return_html)

    def clean_results(self, results: dict):
        """
        Clean the results
        """
        if 'results' in results:
            return results['results']
        elif 'documents' in results:
            return results['documents']
        return results

    def access_field_across_documents(self, f, docs, missing_treatment="return_empty_string"):
        return [self.get_field(f, d, missing_treatment=missing_treatment) for d in docs]

    def convert_concat_list_to_html(self, list_input):
        string = '<div class="row">'
        for x in list_input:
            string += '<div class="column">' + x + '</div>'
        string += "</div>"
        return string

    def render_chunk(self, row, render_func):
        concat_images = [render_func(x) for x in row]
        return self.convert_concat_list_to_html(concat_images)

    def render_image_chunk(self, row, image_width=120):
        render_image_chunks = partial(self.render_image_in_html, image_width=image_width)
        return self.render_chunk(row, render_image_chunks)

    def render_audio_chunk(self, row):
        return self.render_chunk(row, self.render_audio_in_html)

def show_json(json: dict, text_fields: List[str]=[], image_fields: List[str]=[],
        audio_fields: List[str]=[], chunk_image_fields: List[str]=[], chunk_audio_fields: List[str]=[],
        nrows: int=None, image_width: int=60, include_vector=False, return_html: bool=False, missing_treatment: str='return_empty_string',
        highlight_fields={}):
    v = Viewer()
    return v.show_json(json=json, text_fields=text_fields, image_fields=image_fields,
        audio_fields=audio_fields, chunk_image_fields=chunk_image_fields, 
        chunk_audio_fields=chunk_audio_fields,
        nrows=nrows, image_width=image_width, include_vector=include_vector, 
        return_html=return_html, missing_treatment=missing_treatment, 
        highlight_fields=highlight_fields)
