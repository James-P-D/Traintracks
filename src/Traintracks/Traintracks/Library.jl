CELL_EMPTY = 0
CELL_HORIZONTAL = 1
CELL_VERTICAL = 2
CELL_TOP_LEFT = 3
CELL_TOP_RIGHT = 4
CELL_BOTTOM_RIGHT = 5
CELL_BOTTOM_LEFT = 6

function check_board(cell_cols, cell_rows, top_numbers, right_numbers, grid)
	for col = 1:cell_cols
		println("checking col ", col)
		total = 0
	    for row = 1:cell_rows
			if (grid[col, row] != CELL_EMPTY)
				total += 1
			end
		end 
		if (top_numbers[col] != total)
			println("fail expected ", top_numbers[col], " but got", total)
			return false
		else
			println("Success")
		end
    end

	for row = 1:cell_rows
		println("checking row ", row)
		total = 0
	    for col = 1:cell_cols
			if (grid[col, row] != CELL_EMPTY)
				total += 1
			end
		end 
		if (right_numbers[row] != total)
			println("fail expected ", right_numbers[row], " but got", total)
			return false
		else
			println("Success")
		end
    end

	return true
end

function solve(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid)
    println("cell_cols = ", cell_cols)
    println("cell_rows = ", cell_rows)
	
    println("top_numbers = ", top_numbers)
    println("right_numbers = ", right_numbers)
	
	println("start_terminal = ", start_terminal)
	println("end_terminal = ", end_terminal)
	
	println("grid = ", grid)
	
	#for col = 1:cell_cols, row = 1:cell_rows
    #    println(some_array[col, row])
    #end

	return check_board(cell_cols, cell_rows, top_numbers, right_numbers, grid)
end