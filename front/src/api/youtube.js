import axios from 'axios'

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const BASE_URL = 'https://www.googleapis.com/youtube/v3'

export const searchVideos = async (query) => {
    try {
        const response = await axios.get(`${BASE_URL}/search`, {
            params: {
                part: 'snippet',
                q: query,
                key: API_KEY,
                type: 'video',
                maxResults: 12
            }
        })
        return response.data.items
    } catch (error) {
        console.error('YouTube API Error:', error)
        throw error
    }
}

export const getVideoDetails = async (videoId) => {
    try {
        const response = await axios.get(`${BASE_URL}/videos`, {
            params: {
                part: 'snippet',
                id: videoId,
                key: API_KEY
            }
        })
        return response.data.items[0]
    } catch (error) {
        console.error('YouTube API Error:', error)
        throw error
    }
}