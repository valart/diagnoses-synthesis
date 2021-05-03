from parsing import get_model
from pyvis.network import Network


def show_graph(age, sex):
    got_net = Network(height="100%", width="100%", bgcolor="#222222", font_color="white", directed=True)
    got_net.barnes_hut()

    sources = []
    targets = []
    weights = []

    model = get_model()

    # 1 level
    for chapter in model.graph['INITIAL']:
        sources.append('INITIAL')
        targets.append(chapter.code)
        weights.append(chapter.age[age][sex])

        # 2 level
        if chapter.code not in model.graph:
            continue
        for subchapter in model.graph[chapter.code]:
            sources.append(chapter.code)
            targets.append(subchapter.code)
            weights.append(subchapter.age[age][sex])

            # 3 level
            if subchapter.code not in model.graph:
                continue
            for section in model.graph[subchapter.code]:
                sources.append(subchapter.code)
                targets.append(section.code)
                weights.append(section.age[age][sex])

                if section.next is not None:
                    for n in section.next:
                        sources.append(section.code)
                        targets.append(n)
                        weights.append(section.next[n])

                # 4 level
                if section.code not in model.graph:
                    continue
                for subsection in model.graph[section.code]:
                    sources.append(section.code)
                    targets.append(subsection.code)
                    weights.append(subsection.age[age][sex])

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w, title=w)

    neighbor_map = got_net.get_adj_list()

    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    got_net.show("graph.html")
