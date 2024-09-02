import streamlit as st
import requests

# URL da logo
logo_url = "https://res.cloudinary.com/dyykoh8t4/image/upload/v1710548053/Resolve/image1_ugrpkk.png"

# Exibir a logo
st.image(logo_url, width=200)

# Título do aplicativo
st.title("Resolve Agentes")

def get_agents():
    try:
        response = requests.get("https://dash.resolvenergiasolar.com/api/v1/agents")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_tools(agent_id):
    try:
        response = requests.get(f"https://dash.resolvenergiasolar.com/api/v1/agents/{agent_id}/tools")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def ask_agent_with_tool(agent_id, tool_name, query):
    payload = {
        "tool_name": tool_name,
        "query": query
    }
    try:
        response = requests.post(f"https://dash.resolvenergiasolar.com/api/v1/agents/{agent_id}/use-tool", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "Failed to get response"}

with st.spinner("Carregando agentes..."):
    agents = get_agents()

if agents:
    agent_names = [agent['role'] for agent in agents]
    selected_agent = st.selectbox("Selecione um Agente", agent_names)
    agent_id = agents[agent_names.index(selected_agent)]['id']

    with st.spinner("Carregando ferramentas..."):
        tools = get_tools(agent_id)
    
    if tools:
        tool_names = [tool['name'] for tool in tools]
        selected_tool = st.selectbox("Selecione uma Ferramenta", tool_names)

        query = st.text_input("Faça uma pergunta ao agente:")
        if st.button("Enviar"):
            if query.strip():
                response = ask_agent_with_tool(agent_id, selected_tool, query)
                if "error" in response:
                    st.error(response["error"])
                else:
                    st.write(response.get("response", "Resposta não encontrada."))
            else:
                st.warning("A pergunta não pode estar em branco.")
    else:
        st.write("Nenhuma ferramenta disponível para este agente.")
else:
    st.write("Nenhum agente disponível.")
