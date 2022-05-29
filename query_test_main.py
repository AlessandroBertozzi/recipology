from owlready2 import get_ontology, default_world

go = get_ontology("data/tmp_ontology/definitiveversion_3.owl").load()


a=list(default_world.sparql("""
           SELECT ?x
           { ?x rdfs:label "Alici_marinate" .
         }
    """))
#definitiveversion_3.Spaghettoni
print(a)

    # Lasagna -(hasSelectionOperation)> Lasagna_selection_opertion - il> lasagna_selection_operation_1 -> has quantity and hasingredient 