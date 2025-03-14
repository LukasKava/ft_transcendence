import axiosInstance from './axiosInstance';

const baseUrl = process.env.REACT_APP_BACKEND_URL;
const URL = `${baseUrl}/api/users/`;

export const fetchUsers = async () => {
    try {
        const response = await axiosInstance.get(URL, {
            headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'JWT ' + localStorage.getItem('access_token'),
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching users:", error);
        throw error;
    }
};

export default { fetchUsers };
