package models

// Tests commented out to avoid database dependencies

// These tests require database connections and are commented out for now
// In a real implementation, they would use test databases

// func TestUser_GetUserCount(t *testing.T) {
// 	// This would require a database connection in a real test
// 	// For now, we'll test the method exists and doesn't panic
// 	repo := &UserRepository{}
// 	
// 	// Test that the method exists and returns a number
// 	count, err := repo.GetUserCount()
// 	assert.NoError(t, err)
// 	assert.GreaterOrEqual(t, count, 0)
// }

// func TestUser_DeactivateUser(t *testing.T) {
// 	repo := &UserRepository{}
// 	
// 	// Test deactivating a user
// 	err := repo.DeactivateUser(1)
// 	// In a real test, this would require a database
// 	// For now, we just test that the method exists
// 	assert.NoError(t, err)
// }

// func TestUser_ActivateUser(t *testing.T) {
// 	repo := &UserRepository{}
// 	
// 	// Test activating a user
// 	err := repo.ActivateUser(1)
// 	// In a real test, this would require a database
// 	// For now, we just test that the method exists
// 	assert.NoError(t, err)
// }