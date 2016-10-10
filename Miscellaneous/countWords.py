"""Count words."""

def count_words(s, n):
    """Return the n most frequently occuring words in s."""
    
    # TODO: Count the number of occurences of each word in s
    x = s.split(" ")
    w = dict()
    for i in x:
		if i in w.keys():
			w[i] = w[i]+1
		else:
			w[i] = 1;
	
    y = [(k, v) for k, v in w.iteritems()]

    # TODO: Sort the occurences in descending order (alphabetically in case of ties)
    sorted_by_occurance = sorted(y, key=lambda tup: (-tup[1], tup[0]))#, reverse=(True)
	
    if n > len(sorted_by_occurance):
		n = len(sorted_by_occurance)
    print sorted_by_occurance
    top_n = sorted_by_occurance[:n]
    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    return top_n


def test_run():
    """Test count_words() with some inputs."""
    print count_words("cat bat mat cat bat cat", 3)
    print count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()
