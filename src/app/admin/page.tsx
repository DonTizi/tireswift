// Import necessary libraries and components
'use client'
import React, { useState, useEffect } from 'react';
import Navbar from '@/components/navbar';
import '@/app/admin/page.css'

// Define the interface for a transaction
interface Transaction {
  start_date: string;
  end_date: string;
  vehicle_type: string;
  station: string; // Added station property
}

// Helper function to join CSS classes
function classNames(...classes: (string | boolean)[]) {
  return classes.filter(Boolean).join(' ');
}

// Helper function to create an array of days for a month
function createDaysForMonth(year: number, month: number, daysInMonth: number) {
  return Array.from({ length: daysInMonth }, (_, i) => ({
    date: `${year}-${String(month).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`,
    isCurrentMonth: true,
  }));
}

// Month names
const monthNames: { [key: string]: string } = {
  '10': 'Octobre',
  '11': 'Novembre',
  '12': 'Décembre',
};

export default function Example() {
  const [currentMonth, setCurrentMonth] = useState<string>('10'); // Start with October
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  // Define months with days
  const months: { [key: string]: { date: string; isCurrentMonth: boolean }[] } = {
    '10': createDaysForMonth(2022, 10, 31),
    '11': createDaysForMonth(2022, 11, 30),
    '12': createDaysForMonth(2022, 12, 31),
  };

  // Fetch transactions when selectedDate changes
  useEffect(() => {
    if (selectedDate) {
      fetch(`http://127.0.0.1:5000/transactions?date=${selectedDate}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          console.log('API Response:', data);
          setTransactions(data as Transaction[]);
        })
        .catch((error) => {
          console.error('API Error:', error);
        });
    }
  }, [selectedDate]);

  // Handle date click
  const handleDateClick = (date: string) => {
    setSelectedDate(date);
  };

  // Handle month change
  const handleMonthChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setCurrentMonth(event.target.value);
  };

  return (
    <>
      <Navbar />
      <div className="md:grid md:grid-cols-2 md:divide-x md:divide-gray-200">
        <div className="md:pr-14">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              {monthNames[currentMonth]} 2022
            </h2>
            <select
              value={currentMonth}
              onChange={handleMonthChange}
              className="ml-2 border border-gray-300 rounded-md p-1"
            >
              {Object.keys(monthNames).map((month) => (
                <option key={month} value={month}>
                  {monthNames[month]}
                </option>
              ))}
            </select>
          </div>
          <div className="mt-10 grid grid-cols-7 text-center text-xs leading-6 text-gray-500">
            <div>Dim</div>
            <div>Lun</div>
            <div>Mar</div>
            <div>Mer</div>
            <div>Jeu</div>
            <div>Ven</div>
            <div>Sam</div>
          </div>
          <div className="mt-2 grid grid-cols-7 text-sm">
            {months[currentMonth].map((day, dayIdx) => (
              <div
                key={day.date}
                className={classNames(dayIdx > 6 && 'border-t border-gray-200', 'py-2')}
              >
                <button
                  type="button"
                  onClick={() => handleDateClick(day.date)}
                  className="mx-auto flex h-8 w-8 items-center justify-center rounded-full text-gray-900 hover:bg-gray-200"
                >
                  <time dateTime={day.date}>{day.date.split('-').pop()}</time>
                </button>
              </div>
            ))}
          </div>
        </div>
        <section>
          {selectedDate && (
            <div>
              <h2 className="text-base font-semibold leading-6 text-gray-900">
                Schedule for {selectedDate}
              </h2>
              {transactions.length > 0 ? (
                <div className="transactions-container">
                  {transactions.map((transaction, index) => (
                    <div key={index} className="transaction-card group flex items-center space-x-4 rounded-xl px-4 py-2 focus-within:bg-gray-100 hover:bg-gray-100">
                      <div className="flex-auto">
                        <p className="text-gray-900"><strong>Type of car:</strong> {transaction.vehicle_type}</p>
                        <p className="text-gray-900"><strong>Station:</strong> {transaction.station}</p> {/* Display Station */}
                        <p className="mt-0.5">
                          <time dateTime={transaction.start_date}>{transaction.start_time}</time> -{' '}
                          <time dateTime={transaction.end_date}>{transaction.end_time}</time>
                        </p>
                      </div>
                      <button className="open-options">Open options</button>
                    </div>
                  ))}
                </div>
              ) : (
                <p>Aucune transaction trouvée pour cette date.</p>
              )}
            </div>
          )}
        </section>
      </div>
    </>
  );
}
