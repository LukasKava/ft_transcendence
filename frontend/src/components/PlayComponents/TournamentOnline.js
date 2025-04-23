import React, {useContext} from 'react';
import { useTranslation } from "react-i18next";
import InviteUsersForATournament from './InviteUsersForATournament';
import { AuthContext } from '../../context/AuthContext';
import { GameContext } from "../../context/GameContext";
import	'./PlayMultiplayerMode.css'
import "../../pages/Play.css"

const TournamentOnline = ({ scaleStyle }) => {
    const { t } = useTranslation();
	const { setNavbarOff } = useContext(AuthContext);
	const { setIsReadyToPlay, isOpponentAuthenticated } = useContext(GameContext);

	return (
		<>
			<div className="playCardHolderStyle" style={scaleStyle}> {/*card basic mode"*/}
				<h3 style={scaleStyle}>{t("PlayTitleTournamentOnline")}</h3>
				<p style={scaleStyle} className="playCardDescription">{t("PlayDescriptionTournamentOnline")}</p>
				<InviteUsersForATournament style={scaleStyle}/>
				<button className="buttonStyle1"
						style={scaleStyle} 
						onClick={() => {
							setNavbarOff(true);
							setIsReadyToPlay("multiplayer")
						}} 
						disabled={!isOpponentAuthenticated}
						aria-label={t("Start multiplayer game button")}
				>
                	{t("PlayTournamentOnline")}
            	</button>
			</div>
		</>
	);
};

export default TournamentOnline;