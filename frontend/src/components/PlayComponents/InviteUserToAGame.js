import React, { useState, useContext, useEffect, use } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { GameContext } from "../../context/GameContext";
import { useTranslation } from "react-i18next";
import { authenticateUser } from '../../services/postAuthenticateUser';
import  handle42Authentication  from '../../services/auth42callback';
import './AuthUserForm.css';
import { fetchUsers } from '../../services/fetchUsers';

const Filter = (props) => {
	return (
	  <div>
		<input  className = {props.className}
				placeholder={props.placeholder}
				type={props.type}
				value={props.value}
				onChange={props.onChange}/>
	  </div>
	)
}	
	
const InviteUserToAGame = ({ scaleStyle }) => {
	const { t } = useTranslation();
	const navigate = useNavigate();
	const {
		isOpponentAuthenticated,
		setIsOpponentAuthenticated,
		player2DisplayName,
		setPlayer2DisplayName,
		setPlayer2Id,
		setPlayer1DisplayName,
		setPlayer1Id,
	} = useContext(GameContext);
	const personLoggedIn = localStorage.getItem('user_id');

	const [invitedPlayer, setInvitedPlayer] = useState(null);
	const [query, setQuery] = useState('');
	const [filterUsers, setFilterUsers] = useState([]);
	const [allUsers, setAllUsers] = useState([]);
	
	const [credentials, setCredentials] = useState({ username: '', password: '' });
	const [isBeingSubmitted, setIsBeingSubmitted] = useState(false);
	const [error, setError] = useState('');

	useEffect(() => {
		const fetchAllUsers = async () => {
			try {
				const users = await fetchUsers();
								
				const otherUsers = users.filter(user => user.id !== personLoggedIn);
				setAllUsers(otherUsers);
								
				// const friendsList = otherUsers.filter(user =>
				// 	profileData.friends.includes(user.id)
				// );
				// setFriends(friendsList);
			} catch (error) {
				console.error('Error fetching users:', error);
			}
		};
		fetchAllUsers();
	}, []);

	useEffect(() => {
		const storedError = localStorage.getItem('urlError');
		if (storedError) {
			if (storedError === 'User not found'){
				setError(t('User not found'))
			}else if(storedError === 'You cannot play against yourself'){
				setError(t('You cannot play against yourself'))
			}else
				setError('')
			
			localStorage.removeItem('urlError');
		}
	}, []);

	const handle42AuthClick = () => {
		setError('')
		sessionStorage.setItem('mode', 'match');

		handle42Authentication();
	};
	
	const handleAuthentication = async (e) => {
		e.preventDefault();
		setIsBeingSubmitted(true);
		setError('');

		try {
			const data = await authenticateUser(credentials);

			if (typeof data.user_id === 'number') {
				const personsLoggedInId = Number(localStorage.getItem('user_id'));
				const personsLoggedInDisplayName = localStorage.getItem('display_name');

				if (data.user_id === personsLoggedInId) {
					setError(t('You cannot play against yourself'));
					setIsOpponentAuthenticated(false);
				} else {
					setIsOpponentAuthenticated(true);
					setPlayer2Id(data.user_id);
					setPlayer2DisplayName(data.display_name);
					setPlayer1Id(personsLoggedInId);
					setPlayer1DisplayName(personsLoggedInDisplayName);
					navigate('/play'); 
				}
			} else {
				setError(t('Invalid credentials'));
				setIsOpponentAuthenticated(false);
			}
		} catch (error) {
			setError(t('Authentication failed'));
			setIsOpponentAuthenticated(false);
		} finally {
			setIsBeingSubmitted(false);
		}
	};

	const handleSearch = (event) => {
		const currFiltered = event.target.value;
		setQuery(currFiltered);
		if (!currFiltered) {
		  setFilterUsers([]);
		} else {
		  const filteredUsers = allUsers.filter(user => user.username.toLowerCase().includes(currFiltered.toLowerCase()));
		  setFilterUsers(filteredUsers);
		}
	  };

	if (isOpponentAuthenticated) {
		return (
			<div className="auth-form d-flex flex-column" style={scaleStyle}>
				<h4 style={scaleStyle}>
					{t("You can start the game")} 
				</h4>
				<p>
					{t("You are playing against ")} 
					{player2DisplayName}
				</p>
			</div>
		)
	}

	return (
		<form onSubmit={handleAuthentication} className="auth-form d-flex flex-column" style={scaleStyle}>
			<h4 style={scaleStyle}>
				{t("Invite a player")}
			</h4>
			{invitedPlayer && (
				<div className="authenticated-players" style={scaleStyle}>
						<p>
							{t("Player")} {invitedPlayer}: {t("pending")}
						</p>
				</div>
			)}
			<label style={scaleStyle} className="AuthUser_and_TournamentFormInput_holder">
				{t("Username")}
				<Filter 	
					className="inputFieldStyle1" 
					placeholder={t("Search for users")} 
					type="text" 
					value={query} 
					onChange={handleSearch} 
					aria-label={t("Search for users")} 
		    	/>
				{filterUsers.length > 0 && (
		<ul className="user-dropdown">
			{filterUsers.map((user) => (
				<li
					key={user.id}
					className="dropdown-item"
					onClick={() => {
						setQuery(user.username);
						setFilterUsers([]);
						setCredentials({ ...credentials, username: user.username });
						setInvitedPlayer(user.username);
					}}
				>
					{user.username} 
				</li>
			))}
		</ul>
	)}
			</label>
			<button
				type="submit"
				className="buttonStyle1"
				style={scaleStyle}
				disabled={isOpponentAuthenticated || isBeingSubmitted}
				aria-label={isOpponentAuthenticated ? t("Player is ready") : t("Submit credentials")}
			>
				{isOpponentAuthenticated ? t("Ready") : t("Submit")}
			</button>
			{error && <p className="text-red-500" style={scaleStyle}>{error}</p>}
		</form>
	);
};

export default InviteUserToAGame;
