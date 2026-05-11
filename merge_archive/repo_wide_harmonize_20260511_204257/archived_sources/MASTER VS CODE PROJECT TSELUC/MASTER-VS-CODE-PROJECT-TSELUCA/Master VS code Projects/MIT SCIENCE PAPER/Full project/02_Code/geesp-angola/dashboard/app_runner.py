import streamlit as st
from dashboard.pages import home, data_explore, mcda, results, lcoe

PAGES = {
    "Home": home,
    "Data Exploration": data_explore,
    "MCDA Analysis": mcda,
    "Results": results,
    "LCOE Calculator": lcoe,
}


def main():
    st.sidebar.title("GEESP-Angola")
    choice = st.sidebar.radio("Pages", list(PAGES.keys()))
    page = PAGES[choice]
    page.render()


if __name__ == "__main__":
    main()

# Footer shared across pages
def render_footer():
    st.divider()
    st.markdown(
        """
<div style='text-align: center; color: #888; font-size: 0.9em; margin-top: 3rem;'>
    <p>GEESP-Angola Dashboard | Desenvolvido para MIT Climate Portal 2026</p>
    <p>Autores: Rocélio Da Silva, Alexandre Dos Santos, Delfina Mpanka (ISPTEC)</p>
</div>
""",
        unsafe_allow_html=True,
    )


render_footer()
