import streamlit as st
from llm_agents import consumer_agent


def main():
    st.title("Marketing Simulator")

    st.header("Brand")
    brand_name = st.text_input("Brand Name")
    marketing_messages = st.text_input("Marketing message")

    with st.expander("Add second brand"):
        brand_name2 = st.text_input("Brand Name 2", value="")
        marketing_messages2 = st.text_input("Marketing message 2", value="")

    st.header("Consumer Persona")
    demographic = st.text_input("Demographics")
    interests = st.text_input("Interests")
    habits = st.text_input("Habits")

    with st.form(key='my_form'):
        submit_button = st.form_submit_button(label='Submit')

    brand_names = [brand_name]
    marketing_messages = [marketing_messages]
    if brand_name2 != "" and marketing_messages2 != "":
        brand_names.append(brand_name2)
        marketing_messages.append(marketing_messages2)


    if submit_button:
        output = consumer_agent(
            brand_names, marketing_messages, demographic, interests, habits)

        st.header("Consumer Reaction")
        if len(brand_names) == 1:
            st.write(f"Opinion: {output['opinion']}")
            st.write(f"Sentiment score: {output['sentiment']}")
            st.write(f"Probability of purchase: {output['probability']}")
        else:
            for brand, val in output.items():
                st.write(f"Opinion {brand}: {val['opinion']}")
                st.write(f"Sentiment score {brand}: {val['sentiment']}")
                st.write(f"Probability of purchase {brand}: {val['probability']}")
    return


if __name__ == "__main__":
    main()
