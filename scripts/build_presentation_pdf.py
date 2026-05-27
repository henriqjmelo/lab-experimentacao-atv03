from pathlib import Path
import textwrap

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUTPUT = DOCS / "Relatorio_Lab03_Apresentacao.pdf"


def new_page(figsize=(11.69, 8.27)):
    fig = plt.figure(figsize=figsize)  # A4 landscape
    fig.patch.set_facecolor("white")
    return fig


def draw_wrapped(ax, text, x, y, width=95, size=12, line_gap=0.045):
    for line in textwrap.wrap(text, width=width):
        ax.text(x, y, line, fontsize=size, va="top", ha="left")
        y -= line_gap
    return y


def add_cover(pdf, stats):
    fig = new_page()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.text(0.5, 0.82, "Relatorio de Laboratorio 03", ha="center", va="center", fontsize=30, fontweight="bold")
    ax.text(0.5, 0.74, "Caracterizando a atividade de code review no GitHub", ha="center", va="center", fontsize=18)

    ax.text(0.5, 0.61, "Curso: Engenharia de Software", ha="center", fontsize=13)
    ax.text(0.5, 0.57, "Disciplina: Laboratorio de Experimentacao de Software", ha="center", fontsize=13)

    ax.text(0.5, 0.43, f"PRs analisados: {stats['prs_total']:,}".replace(",", "."), ha="center", fontsize=16)
    ax.text(0.5, 0.39, f"Repositorios: {stats['repos_count']} (validos no dataset: {stats['repos_with_data']})", ha="center", fontsize=14)
    ax.text(0.5, 0.35, f"MERGED: {stats['merged_pct']:.2f}% | CLOSED: {stats['closed_pct']:.2f}%", ha="center", fontsize=14)

    ax.text(0.5, 0.18, "Atualizado em 22/05/2026", ha="center", fontsize=11, color="dimgray")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_summary_page(pdf, stats):
    fig = new_page()
    ax = fig.add_axes([0.06, 0.08, 0.88, 0.84])
    ax.axis("off")

    ax.text(0, 1.0, "Resumo Executivo", fontsize=22, fontweight="bold", va="top")
    y = 0.90

    intro = (
        "Esta analise investiga a relacao entre caracteristicas de Pull Requests "
        "(tamanho, tempo, descricao e interacoes) e dois desfechos: status final "
        "(MERGED/CLOSED) e numero de revisoes."
    )
    y = draw_wrapped(ax, intro, 0.0, y, width=100, size=13, line_gap=0.05)
    y -= 0.03

    bullets = [
        f"Dataset final: {stats['prs_total']:,} PRs e {stats['repos_count']} repositorios (199 com dados validos).".replace(",", "."),
        f"Distribuicao de status: MERGED {stats['merged_pct']:.2f}% e CLOSED {stats['closed_pct']:.2f}%.",
        "Critrios de inclusao dos PRs: status MERGED/CLOSED, reviews >= 1 e duracao >= 1 hora.",
        "Testes estatisticos: Mann-Whitney U (RQ01-RQ04) e Spearman (RQ05-RQ08).",
    ]
    for b in bullets:
        y = draw_wrapped(ax, f"- {b}", 0.0, y, width=98, size=12, line_gap=0.046)
        y -= 0.01

    ax.text(0, y - 0.02, "Principais achados", fontsize=16, fontweight="bold", va="top")
    y -= 0.09
    findings = [
        "PRs MERGED tendem a ser menores e mais rapidos que PRs CLOSED.",
        "Interacoes e tamanho apresentam as maiores associacoes com o numero de revisoes.",
        "Associacoes observadas sao fracas a moderadas; interpretacao deve considerar tamanho de efeito.",
    ]
    for f in findings:
        y = draw_wrapped(ax, f"- {f}", 0.0, y, width=98, size=12, line_gap=0.046)
        y -= 0.01

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_results_page(pdf):
    fig = new_page()
    ax = fig.add_axes([0.05, 0.08, 0.9, 0.84])
    ax.axis("off")
    ax.text(0, 1.0, "Resultados Estatisticos (Resumo)", fontsize=22, fontweight="bold", va="top")

    table_text = [
        ["RQ", "Indicador", "Valor", "Conclusao"],
        ["RQ01", "MWU p-value", "< 0.0001", "Diferenca significativa"],
        ["RQ02", "MWU p-value", "< 0.0001", "Diferenca significativa"],
        ["RQ03", "MWU p-value", "< 0.0001", "Diferenca significativa"],
        ["RQ04", "MWU p-value", "< 0.0001", "Diferenca significativa"],
        ["RQ05", "Spearman (rho)", "0.3428", "Positiva moderada"],
        ["RQ06", "Spearman (rho)", "0.2979", "Positiva fraca/moderada"],
        ["RQ07", "Spearman (rho)", "0.1389", "Positiva fraca"],
        ["RQ08", "Spearman (rho)", "0.4147", "Positiva moderada"],
    ]

    table = ax.table(cellText=table_text[1:], colLabels=table_text[0], cellLoc="center", colLoc="center", bbox=[0, 0.22, 1, 0.68])
    table.auto_set_font_size(False)
    table.set_fontsize(11)

    ax.text(
        0,
        0.12,
        "Nota: com N elevado, significancia estatistica deve ser analisada em conjunto com magnitude de efeito.",
        fontsize=11,
        color="dimgray",
    )
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_image_page(pdf, image_path, title):
    fig = new_page()
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.88])
    ax.axis("off")
    ax.set_title(title, fontsize=18, fontweight="bold", pad=12)

    img = mpimg.imread(str(image_path))
    ax.imshow(img)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def collect_stats():
    repos = pd.read_csv(DOCS / "repositorios_selecionados.csv")
    prs = pd.read_csv(DOCS / "github_prs_data.csv")
    merged = int((prs["state"] == "MERGED").sum())
    closed = int((prs["state"] == "CLOSED").sum())
    total = len(prs)
    return {
        "repos_count": int(len(repos)),
        "repos_with_data": int(prs["repo"].nunique()),
        "prs_total": int(total),
        "merged_pct": (merged / total) * 100,
        "closed_pct": (closed / total) * 100,
    }


def main():
    stats = collect_stats()
    image_specs = [
        (DOCS / "rq01_bar_tamanho_por_status.png", "RQ01 - Tamanho por Status"),
        (DOCS / "rq02_bar_tempo_por_status.png", "RQ02 - Tempo por Status"),
        (DOCS / "rq03_bar_descricao_por_status.png", "RQ03 - Descricao por Status"),
        (DOCS / "rq04_bar_interacoes_por_status.png", "RQ04 - Interacoes por Status"),
        (DOCS / "rq05_tamanho_vs_revisoes.png", "RQ05 - Tamanho vs Revisoes"),
        (DOCS / "rq06_tempo_vs_revisoes.png", "RQ06 - Tempo vs Revisoes"),
        (DOCS / "rq07_descricao_vs_revisoes.png", "RQ07 - Descricao vs Revisoes"),
        (DOCS / "rq08_interacoes_vs_revisoes.png", "RQ08 - Interacoes vs Revisoes"),
    ]

    missing = [str(p.name) for p, _ in image_specs if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Imagens ausentes: {', '.join(missing)}")

    with PdfPages(OUTPUT) as pdf:
        add_cover(pdf, stats)
        add_summary_page(pdf, stats)
        add_results_page(pdf)
        for img_path, title in image_specs:
            add_image_page(pdf, img_path, title)

    print(f"PDF gerado com sucesso: {OUTPUT}")


if __name__ == "__main__":
    main()
