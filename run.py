from flask import Flask, request, jsonify
from nltk.tree import Tree

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

@app.route('/paraphrase', methods=['GET'])
def paraphrase():

    tree_str = request.args.get('tree')
    if not tree_str:
        return jsonify({'error': 'Missing "tree" parameter.'}), 400
    
    try:
        tree = Tree.fromstring(tree_str)
    except ValueError:
        return jsonify({'error': 'Invalid tree string.'}), 400    

    limit = int(request.args.get('limit', 20))
    
    nps = find_nps(tree)
    
    paraphrases = generate_paraphrases(tree, nps, limit)
    
    return jsonify({'paraphrases': [{'tree': str(p)} for p in paraphrases]})


def find_nps(tree):
    nps = []
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        np_str = ' '.join(subtree.leaves())
        nps.append(np_str)
    return nps

def generate_paraphrases(tree, nps, limit):
    paraphrases = set()
    for i, np1 in enumerate(nps):
        for j, np2 in enumerate(nps[i+1:], i+1):
            new_tree = tree.copy(deep=True)
            np1_subtree = find_np_subtree(new_tree, np1)
            np2_subtree = find_np_subtree(new_tree, np2)
            if np1_subtree is not None and np2_subtree is not None:
                swap_nps(np1_subtree, np2_subtree)
                paraphrased_tree = str(new_tree)
                paraphrases.add(paraphrased_tree)
                if len(paraphrases) >= limit:
                    return paraphrases
    return paraphrases


def find_np_subtree(tree, np_str):
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        if ' '.join(subtree.leaves()) == np_str:
            return subtree
    return None

def find_np_subtrees(tree, np1, np2):
    np1_subtree = None
    np2_subtree = None
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        np_str = ' '.join(subtree.leaves())
        if np_str == np1:
            np1_subtree = subtree
        elif np_str == np2:
            np2_subtree = subtree
        if np1_subtree and np2_subtree:
            break
    return np1_subtree, np2_subtree

def swap_nps(np1_subtree, np2_subtree):
    np1_subtree.clear()
    np1_subtree.extend(np2_subtree)
    np2_subtree.clear()
    np2_subtree.extend(np1_subtree)
    
