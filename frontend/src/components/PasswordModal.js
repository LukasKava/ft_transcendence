import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { AccessibilityContext } from '../AccessibilityContext';
import './PasswordModal.css';
import useWindowDimensions from '../components/userWindowDimensions';

const baseUrl = process.env.REACT_APP_BACKEND_URL; // Base URL for the backend
const PasswordModal = ({ isOpen, onClose, onSubmit, onPasswordSuccess }) => {
    const [password, setPassword] = useState('');
	const { t } = useTranslation();
	const { fontSize } = useContext(AccessibilityContext);
	const [error, setError] = useState('');
    const { width, height } = useWindowDimensions();

	const scalestyle = {
        fontSize: `${fontSize}px`,
        lineHeight: '1.5'
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const userId = localStorage.getItem('user_id');

        try {
				const response = await fetch(`${baseUrl}/user_management/otp-activate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    user_id: userId,
                    password: password
                })
            });

						if (!response.ok) {
								const errorData = await response.json();
								if (response.status === 400) {
										if (errorData.non_field_errors && errorData.non_field_errors.includes("Invalid OTP code.")) {
											setError(t('Incorrect OTP code.'));
											if (onPasswordSuccess) onPasswordSuccess();
											return;
										}
										if (errorData.non_field_errors && errorData.non_field_errors.includes("Incorrect password.")) {
												setError(t('Incorrect password.'));
												return;
										}
								}
								throw new Error('Network response was not ok!');
            }

            const data = await response.json();
            localStorage.setItem('qr_code_url', data.qr_code_url);
            onSubmit(password);

            if (onPasswordSuccess) onPasswordSuccess();
        } catch (error) {
            console.error('Error:', error);
        }

        setPassword('');
    };

    if (!isOpen) return null;

    return (
        <div className="tfa-box d-flex align-items-center justify-content-center" style={{minHeight: `${height - 90}px`}}>
            <div className="tfa-box-overlay align-items-center justify-content-center flex-column" style={scalestyle}>
                <h2 className="tfa-title" style={scalestyle}>{t("Confirm Password")}</h2>
                <p className="tfa-message" style={scalestyle}>
                    {t("Please enter your password to confirm this action")}
                </p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="password"
                        value={password}
						autoComplete="off"
						style={scalestyle}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder={t("Enter your password")}
                        className="tfa-input-password"
                        required
						aria-label={t("Enter your password")}
                    />
					{error && <p className="tfa-message">{error}</p>}
                    <div className="tfa-buttons d-flex flex-column-reverse" style={scalestyle}>
                        <button
                            type="button"
							style={scalestyle}
                            onClick={onClose}
                            className="tfa-button"
							aria-label={t("Cancel")}
                        >
                            {t("Cancel")}
                        </button>
                        <button
                            type="submit"
							style={scalestyle}
                            className="tfa-button"
							aria-label={t("Confirm")}
                        >
                            {t("Confirm")}
                        </button>
                    </div>
                </form>
            </div>
		</div>
    );
};

export default PasswordModal;
