from entity_linker import EntityLinker
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

def main():
    entity_linker = EntityLinker()
    gen_result_file(entity_linker.annotate, "query-data-dev-set.xml", "results.xml")

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

    print(tostring(out_webscope))


if __name__ == "__main__":
    main()