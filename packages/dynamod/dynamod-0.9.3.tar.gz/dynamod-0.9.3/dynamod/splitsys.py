from dynamod.core import *
from dynamod.segop import Segop

class Splitsys:
    def __init__(self, model):
        self.model = model
        self.n = len(model.attSystem.attributes)
        self.share = 1
        self.changes = []
        self.childs = None
        self.axis = None
        self.values = None
        self.all_none = [None for i in range(self.n)]

    def copy(self):
        cp = Splitsys(self.model)
        cp.share = self.share
        cp.changes = self.changes.copy() if self.changes is not None else None
        cp.childs = self.childs.copy() if self.childs is not None else None
        cp.axis = self.axis
        cp.values = self.values.copy() if self.values is not None else None
        return cp

    def add_segop(self, segop):
        if segop.change == self.all_none:
            return
        self.add_for(segop.seg, segop.share, segop.change)

    def add_for(self, seg, share, change):
        if self.childs is None:
            self.apply(seg, share, change)
            return
        on = seg[self.axis]
        rseg = [seg[i] if i != self.axis else None for i in range(self.n)]
        childs = []
        for sub in self.childs:
            both, rest = sub.split_maybe(on)
            if both is not None:
                childs.append(both)
                both.add_for(rseg, share, change)
            if rest is not None:
                childs.append(rest)
        self.childs = childs

    def split_maybe(self, mask):
        if mask is None:
            return self, None
        if not isinstance(mask, list):
            mask = [mask]
        both = [i for i in self.values if i in mask]
        rest = [i for i in self.values if i not in mask]
        if len(rest) == 0:
            return self, None
        other = self.copy()
        other.values = rest
        if len(both) == 0:
            return None, other
        self.values = both
        return self, other

    def apply(self, seg, share, change):
        base = self
        for axis in range(self.n):
            on = seg[axis]
            if on is not None:
                sub = base.copy()
                others = base.copy()
                if not isinstance(on, list):
                    on = [on]
                sub.values = on.copy()
                att = self.model.attSystem.attributes[axis]
                others.values = [i for i in range(len(att.values)) if i not in on]
                base.share = 1
                base.changes = None
                base.childs = [sub, others]
                base.axis = axis
                base = sub
        for i in range(len(base.changes)):
            (p, pchange) = base.changes[i]
            if change == pchange:
                base.changes[i] = (p+share, pchange)
                return
        base.changes.append((share, change))

    def build_segops(self, onseg=None):
        if onseg is None:
            onseg = Segop(self.model)
        segops = []
        if self.childs is None:
            total = 1
            for (p, pchange) in self.changes:
                total -= p
                myseg = onseg.copy()
                myseg.change = pchange
                myseg.share = p
                segops.append(myseg)
            if total > 0:
                myseg = onseg.copy()
                myseg.change = [None for i in range(self.n)]
                myseg.share = total
                segops.append(myseg)
        else:
            for sub in self.childs:
                on = sub.values
                if len(on) == 1:
                    on = on[0]
                myseg = onseg.restricted(self.axis, on)
                segops.extend(sub.build_segops(myseg))
        return segops



