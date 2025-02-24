import React, { useContext } from 'react';
import { useTranslation } from "react-i18next";
import { AccessibilityContext } from '../AccessibilityContext';

import './About.css'

const About = () => {
	const {t} = useTranslation();
	const { fontSize } = useContext(AccessibilityContext); 

	return (
		<div className="page-content" style={{ fontSize: `${fontSize}px` }}>
			<h1 className='mt-0' style={{marginBottom: "3rem"}}>{t("AboutTitle")}</h1>
			<div className="aboutPContainer">
				<p>
					{t("AboutT1")}
					{t("AboutT2")}
				</p>
				<p>
					{t("AboutT3")}
					<a href="https://github.com/LukasKava/ft_transcendence" 
						className="footer-link"
						target="_blank" 
						rel="noopener noreferrer"
						aria-label={t("GitHubLinkDescription")}
					>
						Github
					</a>.
				</p>
			</div>
		</div>
	);
};

export default About;
