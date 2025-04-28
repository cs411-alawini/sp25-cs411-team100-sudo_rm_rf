import Link from "next/link";

export default function NavigationBar() {
    return (
        <div style = {{
            width: '100%',
            height: '50px',
            backgroundColor: '#2a7eff',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '0 20px',
        }}>
            <div><Link href="/">Home</Link></div>
            <div><Link href="/account">Account info</Link></div>
            <div><Link href="/drugs">Drugs</Link></div>
            <div><Link href="/add-delete">Manage Medications</Link></div>
        </div>
    )
}