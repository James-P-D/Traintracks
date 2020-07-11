CELL_EMPTY = 0
CELL_HORIZONTAL = 1
CELL_VERTICAL = 2
CELL_TOP_LEFT = 3
CELL_TOP_RIGHT = 4
CELL_BOTTOM_RIGHT = 5
CELL_BOTTOM_LEFT = 6
TOTAL_CELL_STATES = 7

function is_complete(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid)

    function get_next_cell(col, row, visited_grid)
    
        function check_cells(col1, row1, col2, row2, visited_grid)
            next_cells = []
            
            if ((col1 > 0) && (col1 <= cell_cols) && (row1 > 0) && (row1 <= cell_rows) && (!visited_grid[col1, row1]))
                push!(next_cells, (col1, row1))                
            end
            if ((col2 > 0) && (col2 <= cell_cols) && (row2 > 0) && (row2 <= cell_rows) && (!visited_grid[col2, row2]))
                if (!(visited_grid[col2, row2]))
                    push!(next_cells, (col2, row2))
                end
            end
            return next_cells            
        end
        
        state = grid[col, row]
        if (state == CELL_HORIZONTAL)
            return check_cells(col + 1, row, col - 1, row, visited_grid)
        elseif (state == CELL_VERTICAL)
            return check_cells(col, row - 1, col, row + 1, visited_grid)
        elseif (state == CELL_TOP_LEFT)
            return check_cells(col, row - 1, col - 1, row, visited_grid)
        elseif (state == CELL_TOP_RIGHT)
            return check_cells(col, row - 1, col + 1, row, visited_grid)
        elseif (state == CELL_BOTTOM_RIGHT)
            return check_cells(col, row + 1, col + 1, row, visited_grid)
        elseif (state == CELL_BOTTOM_LEFT)
            return check_cells(col, row + 1, col - 1, row, visited_grid)
        end
        return next_cells
    end
    
	for col = 1:cell_cols    
		println("checking col ", col)

		total = 0
	    for row = 1:cell_rows
			if (grid[col, row] != CELL_EMPTY)
				total += 1
			end
		end 
		if (top_numbers[col] != total)
			println("fail expected ", top_numbers[col], " but got ", total)
			return false
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
			println("fail expected ", right_numbers[row], " but got ", total)
			return false
		end
    end

    # Create an array cell_cols-by-cell_rows in size, initialised to false
    visited_grid = fill(false, cell_cols, cell_rows)

    (start_terminal_col, start_terminal_row) = start_terminal
    (end_terminal_col, end_terminal_row) = end_terminal
    col = start_terminal_col + 1
    row = start_terminal_row + 1
    
    while ((col != end_terminal_col + 1) && (row != end_terminal_row + 1))
        visited_grid[col, row] = true
        
        next_cells = get_next_cell(col, row, visited_grid)

        if (length(next_cells) != 1)
            return false
        end
        
        (col, row) = next_cells[1]
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

	return is_complete(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid)
end