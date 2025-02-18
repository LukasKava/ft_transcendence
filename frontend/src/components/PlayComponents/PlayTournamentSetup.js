import React, {useContext} from 'react';
import { useTranslation } from "react-i18next";
import AuthTournamentForm from './AuthTournamentForm';
import { GameContext } from "../../context/GameContext";

const PlayTournamentSetup = ({ scaleStyle }) => {
    const { t } = useTranslation();
	const { isTournamentReady, setStartTheTournament } = useContext(GameContext);

    return (
        <>
            <div className="tournament-setup" style={scaleStyle}>
                    <div className="card basic mode">
                        <h3 style={scaleStyle}>{t("PlayTitleTournament")}</h3>
                        <p style={scaleStyle}>{t("PlayDescriptionTournament")}</p>
                        <AuthTournamentForm scaleStyle={scaleStyle}/>
                        <button className="btn button" 
							style={scaleStyle} 
							onClick={() => setStartTheTournament(true)} 
							disabled={!isTournamentReady}
						>
                            {t("PlayTournament")}
                        </button>
                    </div>
            </div>
        </>
    );
};

export default PlayTournamentSetup;