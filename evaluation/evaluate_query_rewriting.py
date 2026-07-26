from retrieval.query_rewriter import QueryRewriter

queries = [
    "How do I deploy apps?",
    "How do pods talk?",
    "How do I expose svc?",
    "How do I store config?",
    "How do I use k8s secrets?",
]

rewriter = QueryRewriter()

print("\nQuery Rewriting Evaluation")
print("-" * 60)

for q in queries:
    print(f"Original : {q}")
    print(f"Rewritten: {rewriter.rewrite(q)}")
    print()
