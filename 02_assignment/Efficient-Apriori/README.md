### Apriori Algorithm

Apriori is an algorithm for frequent item set mining and association rule learning over transactional databases. It proceeds by identifying the frequent individual items in the database and extending them to larger and larger item sets as long as those item sets appear sufficiently often in the database. The frequent item sets determined by Apriori can be used to determine association rules which highlight general trends in the database: this has applications in domains such as market basket analysis.

We can improve the efficiency of the Apriori Algorithm by using the following techniques -

1. Hash-based technique (hashing itemsets into corresponding buckets): A hash-based
technique can be used to reduce the size of the candidate k-itemsets, Ck , for k > 1.
For example, when scanning each transaction in the database to generate the fre-
quent 1-itemsets, L1, from the candidate 1-itemsets in C1, we can generate all of the
2-itemsets for each transaction, hash (i.e., map) them into the different buckets of
a hash table structure, and increase the corresponding bucket counts (Figure 5.5).
A 2-itemset whose corresponding bucket count in the hash table is below the support
threshold cannot be frequent and thus should be removed from the candidate set.
Such a hash-based technique may substantially reduce the number of the candidate
k-itemsets examined (especially when k = 2).

Advantages
- Useful for pruning itemsets from C2 ( using the unused memeory during generation of L1 ), thereby reducing the size of C2.


### References
1. Data Mining: Concepts and Techniques, 2rd ed. Han and Kamber. Section 5.2.3 Improving the Efficiency of Apriori

