import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
  const backgroundImage = `url("https://assets.cruddur.lol/avatars/${props.user.cognito_user_uuid}.jpg")`;
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div 
        className="profile-avatar" 
        style={styles}
        ></div>
  );
}