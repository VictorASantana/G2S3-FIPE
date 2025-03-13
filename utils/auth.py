import time
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from utils.token_manager import AuthTokenManager
from services.user_register import get_user_by_email

class Authenticator:
  def __init__(
    self,
    allowed_users: list,
    secret_path: str,
    redirect_uri: str,
    token_key: str,
    cookie_name: str = "auth_jwt",
    token_duration_days: int = 1,
  ):
    st.session_state["connected"] = st.session_state.get("connected", False)
    self.allowed_users = allowed_users
    self.secret_path = secret_path
    self.redirect_uri = redirect_uri
    self.auth_token_manager = AuthTokenManager(
      cookie_name=cookie_name,
      token_key=token_key,
      token_duration_days=token_duration_days,
    )
    self.cookie_name = cookie_name
    self.is_valid = None

  def _initialize_flow(self) -> google_auth_oauthlib.flow.Flow:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      self.secret_path,
      scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
      ],
      redirect_uri=self.redirect_uri,
    )
    return flow

  def get_auth_url(self) -> str:
    flow = self._initialize_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    return auth_url

  def login(self):
      if not st.session_state["connected"]:
        auth_url = self.get_auth_url()
        st.markdown(f'<a href="{auth_url}" target="_self" style="display: inline-block; padding: 0.5rem 1rem; font-weight: 400; text-align: center; text-decoration: none; border-radius: 0.25rem; color: rgb(255, 255, 255); background-color: rgb(19, 23, 32); border: 1px solid rgba(250, 250, 250, 0.2); cursor: pointer;">Entre com google</a>', unsafe_allow_html=True)

  def check_auth(self):
    if st.session_state["connected"]:
      st.toast(":green[user is authenticated]")
      return

    if st.session_state.get("logout"):
      st.toast(":green[user logged out]")
      return

    token = self.auth_token_manager.get_decoded_token()

    if token is not None:
      st.query_params.clear()
      st.session_state["connected"] = True
      validate_user = get_user_by_email(token["email"])
      st.session_state["user_info"] = {
          "email": token["email"],
          "oauth_id": token["oauth_id"],
          "name": validate_user["user_name"],
          "role": validate_user["role"],
          "user_id": validate_user["user_id"]
      }
      st.rerun()  # update session state

    time.sleep(1)  # important for the token to be set correctly
    auth_code = st.query_params.get("code")
    st.query_params.clear()

    if auth_code:
      flow = self._initialize_flow()
      flow.fetch_token(code=auth_code)
      creds = flow.credentials

      oauth_service = build(serviceName="oauth2", version="v2", credentials=creds)
      user_info = oauth_service.userinfo().get().execute()
      oauth_id = user_info.get("id")
      email = user_info.get("email")
      validate_user = get_user_by_email(email)

      if email in self.allowed_users and validate_user:
        self.auth_token_manager.set_token(email, oauth_id)
        st.session_state["connected"] = True
        st.session_state["user_info"] = {
          "oauth_id": oauth_id,
          "email": email,
          "name": validate_user["user_name"],
          "role": validate_user["role"],
          "user_id": validate_user["user_id"]
        }
        self.is_valid = True
        
      else:
        st.toast(":red[access denied: Unauthorized user]")
        self.is_valid = False

  def logout(self):
    st.session_state["logout"] = True
    st.session_state["user_info"] = None
    st.session_state["connected"] = None
    self.auth_token_manager.delete_token()

def check_required_role(role):
  if "user_info" not in st.session_state or not st.session_state["user_info"]:
    st.error("Você precisa estar logado.")
    st.stop()
  
  if st.session_state["user_info"].get("role") != role:
    st.error("Acesso negado: você não tem permissão para acessar esta página.")
    st.stop()

def get_logged_in_user_id():
    if "user_info" in st.session_state and st.session_state["user_info"]:
        user_data = get_user_by_email(st.session_state["user_info"]["email"])
        return user_data.get("user_id") if user_data else None
    return None
