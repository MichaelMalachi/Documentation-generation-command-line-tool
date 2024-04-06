/* * * * * * * * * * * *
 * File: native_connection.h
 * Description: Native tcp connection header.
 *
 * Created 03/04/2024 by longPtrCall.
 * Changelog:
 * - 03/04/2024 by longPtrCall - Initial version of the file.
 *
 * Made by Illusion.
 * * */

// Internal incldues.
#include <core/network/native_socket.h>
#include <core/types.h>


/* * *
 * @Function - read data from a native connection.
 * @Param _this - native connection instance.
 * @Param _buff - destination buffer.
 * @Param _size - amount of bytes to read.
 * @Returns a real amount of bytes read.
 */
u64 native_connection_read(const native_connection_t* _this, u8* _buff, const u64 _size);

/* * * The end of source file * * */
