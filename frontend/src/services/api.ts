const API_URL = ''
export async function getPayments() {
    const response = await fetch(`/api/payments`)

    if(!response.ok) {
        throw new Error('Failed to fetch payments')
    }

    return response.json()
}