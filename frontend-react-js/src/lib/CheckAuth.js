import { Auth } from 'aws-amplify';

  // check if we are authenicated
export async function getAccessToken(){

  Auth.currentSession()
  .then((cognito_user_session) => {
    const access_token = cognito_user_session.accessToken.jwtToken
    localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken)
  })
  .catch((err) => console.log(err));
}

export async function checkAuth(setUser){
  Auth.currentAuthenticatedUser({

    bypassCache: false 
  })
  .then((cognito_user) => {
    console.log("cognito_user", cognito_user)
    setUser({
      cognito_user_uuid: cognito_user.attributes.sub,
      display_name: cognito_user.attributes.name,
      handle: cognito_user.attributes.preferred_username
    })
    return Auth.currentSession()
  }).then((cognito_user_session) => {
    localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken)
  })
  .catch((err) => console.log(err));
};

