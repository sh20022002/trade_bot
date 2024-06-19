import streamlit as st

def client_page(user):
    """
    This function displays the client page of the SmartTraid application.
    
    Parameters:
    - user: User object representing the current user
    - compenies: List of available stock companies
    
    Returns:
    None
    """
    st.title("SmartTraid")
    st.title("The Future of Trading.")
    st.sidebar.title("Analyze Stock")
    options = st.sidebar.toggle("protfolio/s&p500", True)
    if options:
        st.sidebar.title("protfolio")
        stock_ticker = st.sidebar.selectbox("stock", user.protfolio)
    else:
        st.sidebar.title("s&p500")
        stock_ticker = st.sidebar.selectbox("stock", compenies)
    
    inicaitors = st.sidebar.multiselect('Inicaitors', ['Volume','sma-50', 'EMA', 'ADX', 'RSI'])
    interval = st.sidebar.radio('Interval', ['Day', 'Hour'])
    if interval == 'Day':
        interval = '1d'
    else:
        interval = '1h'
    
    st.sidebar.title("account")
    st.sidebar.write(f"Name: {user.name}")
    st.sidebar.write(f"ID: {user.ID} ")
    st.write(f"Stock: {stock_ticker}")
    st.write(f"Cash: {user.cash}")

    
    if st.button('withdraw'):
        amount = st.number_input("Amount", 1)
        response = client.send_request('withdraw', {'amount': amount})
        if response['status'] == 'success':
            st.write(f"withdraw: {amount}")
            user.cash -= amount


    if st.button("Deposit"):
        amount = st.number_input("Amount", 1)
        response = client.send_request('deposit', {'amount': amount})
        if response['status'] == 'success':
            user.cash += amount
            st.write(f"Deposited: {amount}")
    
    
    for compeny in stocks:
        if compeny.symbol == stock_ticker:
            st.write(f"Name: {compeny.compeny_name}")
            st.plotly_chart(compeny.show(interval, inicaitors))
            st.write(f"Location: {compeny.Location}")
            st.write(f"Founded: {compeny.Founded}")
            st.write(f"CIK: {compeny.CIK}")
            st.write(f"GICS Sector: {compeny.GICS_Sector}")
            st.write(f"GICS Sub-Industry: {compeny.GICS_Sub_Industry}")
            st.write(f"Price: {compeny.price}")

            for open_position in user.open_positions:
                if open_position.symbol == stock_ticker:
                    st.write(f"Amount: {open_position.amount}")
                    st.write(f"Price: {open_position.value}")
                    st.write(f"Total Price: {open_position.total_price}")

            if st.button("Buy"):
                amount = st.number_input("Amount", 1)
                response = client.send_request('buy', {'symbol': stock_ticker, 'amount': amount})
                if response['status'] == 'success':
                    st.write(f"Bought {amount} shares of {stock_ticker}")

            if st.button("Sell"):
                amount = st.number_input("Amount", 1)
                response = client.send_request('sell', {'symbol': stock_ticker, 'amount': amount})
                if response['status'] == 'success':
                    st.write(f"Sold {amount} shares of {stock_ticker}")
            
            # st.write(f"Sentiment: {compeny.sentiment}")
            # st.write(f"Summary: {compeny.summary}")


    exit_app = st.button("Shut Down")
    if exit_app:
        time.sleep(5)
        keyboard.press_and_release('ctrl+w')
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()
#st.sidebar.radio('Interval', ['Day', 'Hour'])

