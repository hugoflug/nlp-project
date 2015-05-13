from entity_linker import EntityLinker
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring

def main():
    entity_linker = EntityLinker()
    gen_result_file(entity_linker.annotate, "test-set.xml", "results.xml")

def gen_result_file(annotate_func, queries_file, output_filename):
    """
        generate a results file in XML for annotating the queries in 'queries_file' using
        the 'annotate_func'
    """
    domtree = xml.dom.minidom.parse(queries_file)
    collection = domtree.documentElement

    out_webscope = Element("webscope")

    sessions = collection.getElementsByTagName("session")
    for session in sessions:
        out_session = SubElement(out_webscope, "session", {"id": session.getAttribute("id")})

        queries = session.getElementsByTagName("query")
        for query in queries:
            out_query = SubElement(out_session, "query", {"starttime": query.getAttribute("starttime")})

            in_text = query.getElementsByTagName("text")[0].firstChild.nodeValue
            out_text = SubElement(out_query, "text")
            out_text.text = "![CDATA[" + in_text + "]]"

            annotations = annotate_func(in_text)

            for annotation in annotations:
                out_annotation = SubElement(out_query, "annotation")
                
                out_span = SubElement(out_annotation, "span")
                out_span.text = "![CDATA[" + annotation.substring + "]]"

                out_target = SubElement(out_annotation, "target")
                out_target.text = "![CDATA[http://en.wikipedia.org/wiki/" + annotation.candidate_entities[0].entity_id + "]]"


    ElementTree(out_webscope).write(output_filename)


if __name__ == "__main__":
    main()