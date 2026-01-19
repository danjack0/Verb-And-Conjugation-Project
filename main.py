from mlconjug3 import Conjugator
import spacy
import sys
from rich.console import Console
from rich.table import Table

console = Console()

try:
    nlp = spacy.load("it_core_news_md")
except OSError:
    console.print("[bold red]Error:[/bold red] Italian language model not found.")
    console.print("Please run: [cyan]python -m spacy download it_core_news_md[/cyan]")
    sys.exit(1)

IRREGULAR_ITALIAN_VERBS = {
    "essere", "avere", "andare", "venire", "uscire", "dire", "bere",
    "stare", "fare", "dare", "volere", "potere", "dovere", "sapere",
    "tenere", "rimanere", "salire", "scegliere", "cogliere", "trarre", 
    "porre", "morire", "sedere",
}

TENSE_CODES = {
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

def extract_and_group_verbs(text):
    """
    Docstring for extract_and_group_verbs
    
    :param text: Description
    """
    ere_list = []
    are_list = []
    ire_list = []
    irregular_list = []
    verb_frequency = {}

    doc = nlp(text.strip())
    freq = doc.count_by(spacy.attrs.LEMMA)
    seen = set()

# Extract and categorize verbs
    for token in doc:
        if token.pos_ in ("VERB", "AUX"):
            lemma = token.lemma_.lower()
            
            if lemma not in seen:
                # Store frequency
                lemma_id = doc.vocab[lemma].orth
                verb_frequency[lemma] = freq.get(lemma_id, 1)
                
                # Categorize by ending
                if lemma in IRREGULAR_ITALIAN_VERBS:
                    irregular_list.append(lemma)
                elif lemma.endswith("are"):
                    are_list.append(lemma)
                elif lemma.endswith("ere"):
                    ere_list.append(lemma)
                elif lemma.endswith("ire"):
                    ire_list.append(lemma)
                
                seen.add(lemma)

    # Sort by frequency (most common first)
    ere_list.sort(key=lambda v: verb_frequency[v], reverse=True)
    are_list.sort(key=lambda v: verb_frequency[v], reverse=True)
    ire_list.sort(key=lambda v: verb_frequency[v], reverse=True)
    irregular_list.sort(key=lambda v: verb_frequency[v], reverse=True)

    # Group into daily study sets
    lists = [ere_list, are_list, ire_list, irregular_list]
    days = [[]]

    def add_to_current_day(item):
        days[-1].append(item)

    def start_new_day():
        days.append([])

    # Create balanced study days
    while any(lists):
        day_has_verbs = False
        
        # Add up to 3 of each regular type
        for verb_list in [ere_list, are_list, ire_list]:
            for _ in range(min(3, len(verb_list))):
                if verb_list:
                    add_to_current_day(verb_list.pop(0))
                    day_has_verbs = True

        # Add 1 irregular
        if irregular_list:
            add_to_current_day(irregular_list.pop(0))
            day_has_verbs = True

        # Start new day if we added any verbs
        if day_has_verbs and any(lists):
            start_new_day()
        else:
            break
    # Remove last day if empty
    if not days[-1]:
        days.pop()

    return days, verb_frequency

def conjugate_italian(verb, selected_codes, frequency=None):
    conj = Conjugator(language="it")
    conjugated = conj.conjugate(verb)

    
    header = f"[bold yellow]{verb.upper()}[/bold yellow]"
    if frequency:
        header += f" [dim](appears {frequency}x)[/dim]"
    console.print(f"\n{header}")
    console.print("─" * 50)

    tempi = [TENSE_CODES[code] for code in selected_codes if code in TENSE_CODES]
    
    for modo, tempo in tempi:
        console.print(f"\n[cyan]{tempo}[/cyan]:")
        if tempo in conjugated.conjug_info[modo]:
            for persona, forma in conjugated.conjug_info[modo][tempo].items():
                console.print(f"  {persona}: [green]{forma}[/green]")

def display_tense_options():
    console.print("\n[bold]Available Tenses:[/bold]")
    console.print("[cyan]Indicativo:[/cyan] 1a-presente, 1b-imperfetto, 1c-passato remoto, 1d-futuro")
    console.print("[cyan]Congiuntivo:[/cyan] 2a-presente, 2b-imperfetto, 2c-passato, 2d-trapassato")
    console.print("[cyan]Condizionale:[/cyan] 3a-presente, 3b-passato")

def main():
        console.print("[bold magenta]Italian Verb Study Organizer[/bold magenta]\n")
        
        # Load text from file or use default
        if len(sys.argv) > 1:
            try:
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                    text_input = f.read()
                console.print(f"[green]✓[/green] Loaded text from: {sys.argv[1]}\n")
            except FileNotFoundError:
                console.print(f"[red]Error:[/red] File '{sys.argv[1]}' not found.")
                sys.exit(1)
        else:
            # Default sample text
            text_input = """Quella mattina, Marco si svegliò più tardi del solito. Aveva promesso di aiutare sua sorella con alcuni documenti, ma non riusciva a trovare la motivazione per alzarsi dal letto. Dopo qualche minuto, decise che sarebbe uscito comunque: «Se rimango qui, perdo tutta la giornata», mormorò.

    Quando arrivò in cucina, sua madre stava preparando il caffè. «Hai dormito bene?», chiese lei. Marco annuì, anche se in realtà aveva passato parte della notte a pensare al suo futuro. «Sì, sì… ora esco un po'. Torno per pranzo.»

    Per strada, incontrò un suo vecchio amico, Davide, che stava correndo per non perdere l'autobus."""
            console.print("[dim]Using default sample text...[/dim]\n")
        
        # Extract and organize verbs
        console.print("[cyan]Analyzing text...[/cyan]")
        days_of_verbs, verb_frequency = extract_and_group_verbs(text_input)
        
        # Display summary
        total_verbs = sum(len(day) for day in days_of_verbs)
        console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
        console.print(f"Found [bold]{total_verbs}[/bold] unique verbs")
        console.print(f"Organized into [bold]{len(days_of_verbs)}[/bold] study days")
        
        # Show frequency table of top 10 verbs
        table = Table(title="Top 10 Verbs by Frequency")
        table.add_column("Verb", style="cyan", no_wrap=True)
        table.add_column("Frequency", style="magenta")
        top_verbs = sorted(verb_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        for verb, freq in top_verbs:
            table.add_row(verb, str(freq))
        console.print(table)
        
        # Ask if user wants to proceed
        proceed = console.input("\n[bold]Proceed with conjugation study?[/bold] (y/n): ")
        if proceed.lower() != 'y':
            console.print("Exiting. Run again when ready to study!")
            return
        
        # Select tenses
        display_tense_options()
        tense_input = console.input("\n[bold]Select tenses[/bold] (comma-separated, e.g., 1a,2a): ")
        selected_codes = [x.strip() for x in tense_input.split(",")]
        
        # Display conjugations for each day
        for i, day in enumerate(days_of_verbs, 1):
            console.print(f"\n{'='*60}")
            console.print(f"[bold cyan]DAY {i}[/bold cyan] [dim]({len(day)} verbs)[/dim]")
            console.print('='*60)
            
            for verb in day:
                conjugate_italian(verb, selected_codes, verb_frequency.get(verb))
            
            if i < len(days_of_verbs):
                continue_input = console.input("\n[dim]Press Enter for next day (or 'q' to quit): [/dim]")
                if continue_input.lower() == 'q':
                    break
        
        console.print("\n[bold green]Study session complete! Buono studio! 📚[/bold green]")

if __name__ == "__main__":
    main()