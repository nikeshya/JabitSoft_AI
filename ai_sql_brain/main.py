from brain import Brain

def run():

    print("""
=================================================
 🧠 AI DATABASE BRAIN — SQLITE VERSION
=================================================
Type 'exit' to quit.
""")

    brain = Brain()

    while True:

        q = input("\nAsk DB > ")

        if q.lower() in ["exit","quit"]:
            break

        result = brain.execute(q)

        print("\nResult:\n", result)

if __name__ == "__main__":
    run()
