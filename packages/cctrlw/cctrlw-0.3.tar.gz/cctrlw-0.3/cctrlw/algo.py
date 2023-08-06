#  %%
from string import printable as _P
import sys
from json import loads
from typing import Dict

class dsu:
    """
    https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    Some implementations here have bad asymptotic complexity, that's ok:
    sets this dsu will be used on are comically small.
    """

    def __init__(self, s=None):
        self.p = s or {}

    def _ensure_exist(self, x):
        return self.p.setdefault(x, x)

    def as_set_of_sets(self, set=frozenset):
        R = {}
        for u in list(self.p.keys()):
            v = self._find(u)
            R.setdefault(
                v,
                {
                    v,
                },
            ).add(u)
        return set(set(S) for S in R.values())

    def get_U(self, set=frozenset):
        S = self.as_set_of_sets(set)
        if S:
            return set.union(*S)
        else:
            return set()

    def get_set_of(self, y, set=frozenset):
        S = self.as_set_of_sets()
        for x in S:
            if y in x:
                return x
        return set(
            {
                y,
            }
        )

    def __repr__(self):
        P = set(_P.encode("utf-8"))
        S, R, t_card, U = self.as_set_of_sets(), [], 0, self.get_U()
        for cur_set in S:
            ss = list(sorted(cur_set))
            if len(ss) == 1:
                continue

            def rep_byte(x):
                c = bytes((x,)).decode("utf-8")
                return f"'{c}'" if x in P else x

            runs, i = [0], 0
            while i != len(ss):
                j = i
                while j < len(ss) and ss[j] == ss[i] + j - i:
                    j += 1
                # [i, j)
                runs.append(j)
                i = j
            r = []
            for i, j in zip(runs, runs[1:]):
                assert j - i > 0
                if j - i == 1:
                    r.append(rep_byte(ss[i]))
                else:
                    r.append(f"{rep_byte(ss[i])}:{rep_byte(ss[j - 1])}")
            r = ", ".join(r)
            r = f'{{{r}}}'
            R.append(r)
            t_card += len(ss)
        singletons = len(U) - t_card
        if singletons:
            R.append(f"<{singletons} singletons ignored>")
        return f"{{{', '.join(R)}}}"

    def union_two(self, x, y):
        for z in (x, y):
            if z not in self.p:
                self.p[z] = z
        self.p[self._find(x)] = self._find(y)

    def union(self, head, *tail):
        for x in tail:
            self.union_two(head, x)

    def _find(self, x):
        self.p.setdefault(x, x)
        if self.p[x] == x:
            return x
        self.p[x] = self._find(self.p[x])
        return self.p[x]

    def clone(self):
        return dsu(dict(self.p))

    def equiv(self, x, y):
        for z in (x, y):
            if z not in self.p:
                self.p[z] = z
        return self._find(x) == self._find(y)


def topsort(adj):
    """
    Return a topological sort of a DAG defined by adjacency list `adj`.
    """
    used, V = {}, set()
    for u, v in adj.items():
        V.add(u)
        V.update(v)
    for u in V:
        used[u] = 0
        if u not in adj:
            adj[u] = []

    def dfs_run(u, g):
        if used[u] == 2:
            return
        used[u] = 1
        for v in g[u]:
            yield from dfs_run(v, g)
        yield u
        used[u] = 2

    ts = []
    for v in V:
        if len(adj[v]) == 1 and not used[v]:
            ts.extend(dfs_run(v, adj))
    ts.reverse()

    ord = {v: i for i, v in enumerate(ts)}
    for u, v in zip(ts[0:], ts[1:]):
        assert (
            ord[u] < ord[v]
        ), "somebody couldn't write a correct topsort; this is a bug, report it"
    return ts


def load_partitions(definitions) -> Dict[str, dsu]:
    """
    Partition <-> dsu aka some partition of the set of all symbols.
    A more convenient way to define mods is as follows: say we have a partition M, and want to derive from it a new partition M', which is strictly less fine than M.
    In M' we want to copy M and union sets containing letters u_1 and v_1, sets containing u_2 and v_2, etc. So
    This is how we define this new partition: (parent, [(u_i, v_i)...]).
    Base case: partition 'S', which is a partition into singletons.
    """
    # group -> [V...]
    adj, p, diff = {}, {}, {}
    for v, (u, d) in definitions.items():
        adj.setdefault(u, []).append(v)
        p[v] = u
        diff[v] = d
    ts, ret = topsort(adj), {}
    S = dsu()
    for x in range(256):
        S.union_two(x, x)
    ret["S"] = S
    for mid in ts:
        if mid == "S":
            continue
        m = ret[p[mid]].clone()
        for u, v in diff[mid]:
            m.union(u, v)
        ret[mid] = m
    return ret


# %%
def get_streak(s: str, m: dsu) -> int:
    """
    Return the length of largest prefix of s that has letters equivalent to first letter with regards to partition m.
    """
    L = 0
    while L < len(s) and m.equiv(s[0], s[L]):
        L += 1
    return L


# %%
if __name__ == "__main__" or "pytest" in sys.modules or "get_ipython" in globals():

    def test_manual():
        dsu0 = dsu()
        dsu0.union(0, 1, 5)
        dsu0.union(2, 3, 7)

        def _get(dsu=dsu0):
            return dsu.as_set_of_sets()

        def C(x):
            return {frozenset(y) for y in x}

        assert _get() == C([[0, 1, 5], [2, 3, 7]])
        print(dsu0.get_set_of(0))
        assert dsu0.get_set_of(0) == {0, 1, 5}
        print(dsu0)
        dsu0.union(5, 3)
        assert _get() == C([[0, 1, 2, 3, 5, 7]])
        print(dsu0)
        print("ok")

    def test_small_random():
        pass  # TODO: implement

    test_small_random()
    test_manual()
