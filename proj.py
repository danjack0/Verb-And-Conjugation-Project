from mlconjug3 import Conjugator
import spacy

nlp = spacy.load("it_core_news_md")

selected_codes = [x.strip() for x in input("Select tenses (comma-separated: (1a,2a,3b): ").split(",")]

IRREGULAR_ITALIAN_VERBS = {
"essere", "avere", "andare", "venire", "uscire", "dire", "bere",
"stare", "fare", "dare",
"volere", "potere", "dovere", "sapere",
"tenere", "rimanere", "salire",
"scegliere", "cogliere", "trarre", "porre",
"morire", "sedere",
}

def spacyFunc(text):

    ere_List = []
    are_List = []
    ire_List = []
    iregular_List = []

    def verb_categorizer (lemma):

        if lemma in IRREGULAR_ITALIAN_VERBS:
            iregular_List.append(lemma)
        elif lemma.endswith("are"):
            are_List.append(lemma)
        elif lemma.endswith("ere"):
            ere_List.append(lemma)
        elif lemma.endswith("ire"):
            ire_List.append(lemma)

        
    doc = nlp(text.strip())

    seen = set()

    for token in doc:
        
        if token.pos_ in ("VERB", "AUX"):
            lemma = token.lemma_.lower()
            
            if lemma not in seen:
                verb_categorizer(lemma)
                seen.add(lemma)

    lists = [ere_List, are_List, ire_List, iregular_List]

    day = [[]]

    def new_day():
        day.append([])

    def add_item(item):
        day[-1].append(item)

    #Create each day w/ 3 verbs from each regular and 1 from irregular
    while all(lists):
            
            if len(ere_List) < 3 or len(are_List) < 3 or len(ire_List) < 3:
                break
            for i in range(3):                  #use xyz_list.pop(0) to get wanted verb
                add_item(ere_List.pop(0))       #and remove from list without messing up iteration
                add_item(are_List.pop(0))
                add_item(ire_List.pop(0))   
            
            if len(iregular_List):
                add_item(iregular_List.pop(0))
            
            new_day()

    if not day[-1]:    #remove last day if empty
        day.pop()
    
    return day


def conjugate_italian(verbIn, selected_codes):
    conj = Conjugator(language="it")
    verb = conj.conjugate(verbIn)

    tense = {
        # Indicativo
        "1a": ("Indicativo", "Indicativo presente"),
        "1b": ("Indicativo", "Indicativo imperfetto"),
        "1c": ("Indicativo", "Indicativo passato remoto"),
        "1d": ("Indicativo", "Indicativo futuro semplice"),
        "1e": ("Indicativo", "Indicativo passato prossimo"),
        "1f": ("Indicativo", "Indicativo trapassato prossimo"),
        "1g": ("Indicativo", "Indicativo trapassato remoto"),
        "1h": ("Indicativo", "Indicativo futuro anteriore"),

        # Congiuntivo
        "2a": ("Congiuntivo", "Congiuntivo presente"),
        "2b": ("Congiuntivo", "Congiuntivo imperfetto"),
        "2c": ("Congiuntivo", "Congiuntivo passato"),
        "2d": ("Congiuntivo", "Congiuntivo trapassato"),

        # Condizionale
        "3a": ("Condizionale", "Condizionale presente"),
        "3b": ("Condizionale", "Condizionale passato"),
    }

    tempi = [tense[code] for code in selected_codes if code in tense]

    for modo, tempo in tempi:
        print(f"\n{tempo} di {verbIn}:")
        if tempo in verb.conjug_info[modo]:
            for persona, forma in verb.conjug_info[modo][tempo].items():
                print(f"{persona}: {forma}")
        else:
            continue


text_input = """Quella mattina, Marco si svegliò più tardi del solito. Aveva promesso di aiutare sua sorella con alcuni documenti, ma non riusciva a trovare la motivazione per alzarsi dal letto. Dopo qualche minuto, decise che sarebbe uscito comunque: «Se rimango qui, perdo tutta la giornata», mormorò.

Quando arrivò in cucina, sua madre stava preparando il caffè. «Hai dormito bene?», chiese lei. Marco annuì, anche se in realtà aveva passato parte della notte a pensare al suo futuro. «Sì, sì… ora esco un po’. Torno per pranzo.»

Per strada, incontrò un suo vecchio amico, Davide, che stava correndo per non perdere l’autobus."""

days_of_verbs = spacyFunc(text_input)

for i, day in enumerate(days_of_verbs, 1):
    print(f"\n=== Day {i} ===")
    for verb in day:
        conjugate_italian(verb, selected_codes)